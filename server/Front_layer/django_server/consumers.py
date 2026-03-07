# chat/consumers.py
import asyncio
import json
import logging
import os
from urllib.parse import quote
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorServer
from Core_layer.Chat_package.Classes.ChatService import ChatService
from Core_layer.Answer_package.Classes import GptAnswer

logger = logging.getLogger(__name__)


def _get_messages_sync(chat_id):
    return ChatService.get_messages(chat_id)


def _clean_command_response(response):
    """Убирает |command| из ответа, возвращает список частей."""
    if not response or not isinstance(response, str):
        return []
    parts = response.replace('|command|\n', '\x00').replace('|command|', '\x00').split('\x00')
    return [p.strip() for p in parts if p.strip()]


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer с загрузкой истории и broadcast на все устройства."""

    async def connect(self):
        self.chat_groups = set()  # chat_id, к которым подключен
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'WebSocket соединение установлено'
        }))

    async def disconnect(self, close_code):
        for chat_id in list(self.chat_groups):
            await self.channel_layer.group_discard(f"chat_{chat_id}", self.channel_name)

    async def chat_broadcast(self, event):
        """Получить broadcast от группы и отправить в WebSocket."""
        if event.get('exclude_channel') == self.channel_name:
            return
        await self.send(text_data=json.dumps(event['data'], ensure_ascii=False))

    def _clean_command_response(self, response):
        """Убирает |command| из ответа, возвращает список частей."""
        parts = response.replace('|command|\n', '\x00').replace('|command|', '\x00').split('\x00')
        return [p.strip() for p in parts if p.strip()]

    async def receive(self, text_data):
        try:
            # JSON: load_history, join_chat
            try:
                data = json.loads(text_data)
                if isinstance(data, dict):
                    msg_type = data.get('type')
                    if msg_type == 'load_history':
                        chat_id = data.get('chat_id')
                        if chat_id:
                            await self._join_chat_group(chat_id)
                            messages = await database_sync_to_async(_get_messages_sync)(chat_id)
                            title = await database_sync_to_async(ChatService.get_title)(chat_id)
                            await self.send(text_data=json.dumps({
                                'type': 'history',
                                'chat_id': chat_id,
                                'messages': messages,
                                'title': title or ''
                            }, ensure_ascii=False))
                        return
                    if msg_type == 'join_chat':
                        chat_id = data.get('chat_id')
                        if chat_id:
                            await self._join_chat_group(chat_id)
                        return
                    if msg_type == 'clear_messages':
                        chat_id = data.get('chat_id')
                        if chat_id:
                            await self._join_chat_group(chat_id)
                            await self._broadcast_clear_messages(chat_id)
                        return
                    if msg_type == 'regenerate':
                        chat_id = data.get('chat_id')
                        message_id = data.get('message_id')
                        user = data.get('user')
                        if chat_id and message_id and user:
                            asyncio.create_task(self._process_regenerate(chat_id, message_id, user))
                        return
            except (json.JSONDecodeError, TypeError):
                pass

            # Legacy: user|chat_id|message|content — обрабатываем в фоне для параллельности
            chat_id = None
            if '|message|' in text_data:
                first = text_data.split('|message|')[0].strip()
                first_parts = first.split('|')
                if len(first_parts) >= 2:
                    chat_id = first_parts[1].strip()
            asyncio.create_task(self._process_and_send(text_data, chat_id))
        except Exception as e:
            import traceback
            logger.error(f"Error in receive: {str(e)}\n{traceback.format_exc()}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Произошла ошибка при обработке сообщения',
                'detail': str(e)
            }, ensure_ascii=False))

    async def _process_and_send(self, text_data, chat_id):
        """Обрабатывает сообщение и отправляет ответ — позволяет параллельную обработку разных чатов."""
        try:
            response = await self.process_message(text_data)
            outarr = self._clean_command_response(response)
            for el in outarr:
                if self.is_file_path(el):
                    el = self.convert_file_path_to_url(el)
                is_img = el.startswith('http') or el.startswith('/images/')
                msg_data = {'type': 'chat_message', 'message': el, 'user': 'Misa', 'isImage': is_img}
                if chat_id:
                    msg_data['chat_id'] = chat_id
                await self.send(text_data=json.dumps(msg_data, ensure_ascii=False))
        except Exception as e:
            import traceback
            logger.error(f"Error processing message: {str(e)}\n{traceback.format_exc()}")
            err_payload = {
                'type': 'error',
                'message': 'Произошла ошибка при обработке сообщения',
                'detail': str(e)
            }
            if chat_id:
                err_payload['chat_id'] = chat_id
            await self.send(text_data=json.dumps(err_payload, ensure_ascii=False))

    async def _process_regenerate(self, chat_id, message_id, user):
        """Перегенерировать ответ: обновить сообщение Misa, не добавляя новых."""
        try:
            await self._join_chat_group(chat_id)
            await self._broadcast_typing(chat_id, is_typing=True, exclude_self=True)

            def _do_regenerate():
                try:
                    msg = ChatService.get_message_by_id(chat_id, message_id)
                    db_message_id = message_id
                    if not msg:
                        msgs_db = ChatService.get_messages(chat_id)
                        if len(msgs_db) >= 2 and str(msgs_db[-1].get('user', '')).strip() == 'Misa':
                            db_message_id = str(msgs_db[-1]['id'])
                            msg = ChatService.get_message_by_id(chat_id, db_message_id)
                        if not msg:
                            logger.warning(f"Regenerate: message {message_id} not found in chat {chat_id}")
                            return None, False, "Сообщение не найдено в БД (обновите чат и попробуйте снова)"
                    if str(msg.get('user', '')).strip() != 'Misa':
                        return None, False, "Сообщение не от Misa"
                    msgs = ChatService.get_messages(chat_id)
                    idx = next((i for i, m in enumerate(msgs) if str(m['id']) == str(db_message_id)), -1)
                    if idx < 1:
                        return None, False, "Нет предыдущего сообщения пользователя"
                    prev = msgs[idx - 1]
                    if str(prev.get('user', '')).strip() == 'Misa':
                        return None, False, "Предыдущее сообщение не от пользователя"
                    user_content = str(prev.get('content', '')).strip()
                    if not user_content:
                        return None, False, "Пустой запрос пользователя"
                    GptAnswer.GptAnswer.import_history_from_db(user, chat_id, exclude_last=2)
                    response = MessageMonitorServer.MessageMonitorServer(user=user, message=user_content, chat_id=chat_id).monitor()
                    if not response:
                        return None, False, "Пустой ответ от модели"
                    cleaned = _clean_command_response(response)
                    msg_to_save = '\n\n'.join(cleaned) if len(cleaned) > 1 else (cleaned[0] if cleaned else response)
                    is_img = any(p.startswith('http') or p.startswith('/images/') for p in cleaned)
                    ChatService.update_message_content(chat_id, db_message_id, msg_to_save, is_img)
                    return (msg_to_save, is_img), True, None
                except Exception as e:
                    logger.exception(f"Regenerate _do_regenerate: {e}")
                    return None, False, str(e)

            result, ok, err_msg = await database_sync_to_async(_do_regenerate)()
            if ok and result:
                msg_to_send, is_img = result
                if self.is_file_path(msg_to_send):
                    msg_to_send = self.convert_file_path_to_url(msg_to_send)
                is_img_final = is_img or (isinstance(msg_to_send, str) and (msg_to_send.startswith('http') or msg_to_send.startswith('/images/')))
                await self.channel_layer.group_send(f"chat_{chat_id}", {
                    'type': 'chat_broadcast',
                    'data': {
                        'type': 'message_updated',
                        'chat_id': chat_id,
                        'message_id': message_id,
                        'message': msg_to_send,
                        'user': 'Misa',
                        'isImage': is_img_final,
                    }
                })
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'chat_id': chat_id,
                    'message': 'Ошибка перегенерации',
                    'detail': err_msg or 'Неизвестная ошибка',
                }, ensure_ascii=False))
        except Exception as e:
            import traceback
            logger.error(f"Regenerate error: {str(e)}\n{traceback.format_exc()}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'chat_id': chat_id,
                'message': 'Ошибка перегенерации',
                'detail': str(e),
            }, ensure_ascii=False))
        finally:
            await self._broadcast_typing(chat_id, is_typing=False, exclude_self=True)

    async def _join_chat_group(self, chat_id):
        group = f"chat_{chat_id}"
        if chat_id not in self.chat_groups:
            await self.channel_layer.group_add(group, self.channel_name)
            self.chat_groups.add(chat_id)

    async def process_message(self, message):
        parts = message.split('|message|')
        if len(parts) < 2:
            return "Я не понял ваш запрос"

        if parts[1].strip() == '__NEW_CHAT__':
            # Новый чат — не очищаем историю GPT, т.к. создаётся новая запись в БД
            return ''

        # Формат: user|chat_id|message|content или user|message|content (без chat_id)
        first = parts[0].strip()
        content = parts[1].strip()
        first_parts = first.split('|')
        if len(first_parts) >= 2:
            user = first_parts[0].strip()
            chat_id = first_parts[1].strip()
        else:
            user = first
            chat_id = None

        if chat_id:
            await self._join_chat_group(chat_id)

        # Импорт истории из БД в контекст GPT для данного чата
        if chat_id and user:
            await database_sync_to_async(GptAnswer.GptAnswer.import_history_from_db)(user, chat_id)

        is_image = content.startswith('/images/') or content.startswith('http')
        if chat_id:
            ChatService.save_message(chat_id, user, content, is_image=is_image)
            await self._broadcast_message(chat_id, user, content, is_image, exclude_self=True)
            await self._broadcast_typing(chat_id, is_typing=True, exclude_self=True)
            # Генерация заголовка в фоне — не блокирует ответ Мисы
            if not is_image:
                async def _gen_and_broadcast_title():
                    def _gen():
                        t = GptAnswer.GptAnswer.generate_chat_title_from_message(content)
                        if t and ChatService.update_title(chat_id, t):
                            return t
                        return None
                    title = await database_sync_to_async(_gen)()
                    if title:
                        await self._broadcast_title(chat_id, title)
                asyncio.create_task(_gen_and_broadcast_title())

        try:
            message_monitor = MessageMonitorServer.MessageMonitorServer(user=user, message=content, chat_id=chat_id)
            response = await database_sync_to_async(message_monitor.monitor)()

            if not response:
                return "Я не понял ваш запрос"

            cleaned = self._clean_command_response(response)
            msg_to_save = '\n\n'.join(cleaned) if len(cleaned) > 1 else (cleaned[0] if cleaned else response)
            is_img = any(p.startswith('http') or p.startswith('/images/') for p in cleaned)
            ChatService.save_message(chat_id, 'Misa', msg_to_save, is_image=is_img)
            for el in cleaned:
                await self._broadcast_message(chat_id, 'Misa', el, is_img, exclude_self=True)

            # Генерация контекстного заголовка (как у DeepSeek)
            def _generate_and_save_title():
                msgs = ChatService.get_messages(chat_id)
                if not msgs:
                    return None
                t = GptAnswer.GptAnswer.generate_chat_title(msgs)
                if t and ChatService.update_title(chat_id, t):
                    return t
                return None
            title = await database_sync_to_async(_generate_and_save_title)()
            if title:
                await self._broadcast_title(chat_id, title)

            return response
        finally:
            if chat_id:
                await self._broadcast_typing(chat_id, is_typing=False, exclude_self=True)

    async def _broadcast_typing(self, chat_id, is_typing=True, exclude_self=True):
        """Broadcast индикатора печати Мисы на все устройства."""
        payload = {
            'type': 'chat_broadcast',
            'data': {'type': 'typing', 'chat_id': chat_id, 'isTyping': is_typing}
        }
        if exclude_self:
            payload['exclude_channel'] = self.channel_name
        await self.channel_layer.group_send(f"chat_{chat_id}", payload)

    async def _broadcast_clear_messages(self, chat_id, exclude_self=True):
        """Broadcast очистки сообщений чата на все устройства."""
        payload = {
            'type': 'chat_broadcast',
            'data': {'type': 'messages_cleared', 'chat_id': chat_id}
        }
        if exclude_self:
            payload['exclude_channel'] = self.channel_name
        await self.channel_layer.group_send(f"chat_{chat_id}", payload)

    async def _broadcast_title(self, chat_id, title, exclude_self=False):
        """Broadcast обновления заголовка чата."""
        payload = {
            'type': 'chat_broadcast',
            'data': {'type': 'chat_title', 'chat_id': chat_id, 'title': title}
        }
        if exclude_self:
            payload['exclude_channel'] = self.channel_name
        await self.channel_layer.group_send(f"chat_{chat_id}", payload)

    async def _broadcast_message(self, chat_id, user, content, is_image=False, exclude_self=False):
        """Отправить сообщение всем подключённым к чату (все устройства)."""
        payload = {
            'type': 'chat_broadcast',
            'data': {
                'type': 'chat_message',
                'chat_id': chat_id,
                'message': content,
                'user': user,
                'isImage': is_image,
            }
        }
        if exclude_self:
            payload['exclude_channel'] = self.channel_name
        await self.channel_layer.group_send(f"chat_{chat_id}", payload)

    def is_file_path(self, response):
        if not isinstance(response, str):
            return False

        cleaned_path = response.strip().replace('\n', '')

        if os.path.exists(cleaned_path) and os.path.isfile(cleaned_path):
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
            file_ext = os.path.splitext(cleaned_path)[1].lower()
            return file_ext in image_extensions

        return False

    def convert_file_path_to_url(self, file_path):
        try:
            # Удаляем лишние символы \n и пробелы
            cleaned_path = file_path.strip().replace('\n', '')
            abs_file_path = os.path.abspath(cleaned_path)
            images_dir = os.path.join(settings.BASE_DIR, 'images')

            # Получаем API_URL из настроек Django
            api_url = getattr(settings, 'API_URL', '')

            # Если файл в папке images
            if abs_file_path.startswith(images_dir):
                relative_path = os.path.relpath(abs_file_path, images_dir)
                encoded_path = quote(relative_path.replace('\\', '/'))
                return f"{api_url}/images/{encoded_path}" if api_url else f"/images/{encoded_path}"

            # Если файл в других статических директориях
            for static_dir in settings.STATICFILES_DIRS:
                if abs_file_path.startswith(static_dir):
                    relative_path = os.path.relpath(abs_file_path, static_dir)
                    encoded_path = quote(relative_path.replace('\\', '/'))
                    return f"{api_url}/{encoded_path}" if api_url else f"/{encoded_path}"

            # Если файл в корне проекта
            if abs_file_path.startswith(str(settings.BASE_DIR)):
                relative_path = os.path.relpath(abs_file_path, settings.BASE_DIR)
                encoded_path = quote(relative_path.replace('\\', '/'))
                return f"{api_url}/{encoded_path}" if api_url else f"/{encoded_path}"

            return cleaned_path

        except Exception as e:
            logger.error(f"Error converting file path: {str(e)}")
            return file_path  # Возвращаем оригинальный путь в случае ошибки