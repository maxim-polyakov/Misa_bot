# chat/consumers.py
import asyncio
import json
import logging
import os
from urllib.parse import quote
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from django.core.cache import cache
from Core_layer.Chat_package.Classes.ChatService import ChatService
from Core_layer.Answer_package.Classes import GptAnswer
from Core_layer.Command_package.Classes.Commands import CommandAnalyzer
from Core_layer.Generation_package.service import GenerationService
from Deep_layer.API_package.Classes.GradiusService import GradiusService

logger = logging.getLogger(__name__)

# Статус «Миса печатает» переживает refresh вкладки / reconnect (Redis или locmem)
_GENERATING_CACHE_TTL = 600  # сек
_AD_ENRICHMENT_CACHE_TTL = 600


def _generating_cache_key(chat_id):
    return f"misa:chat_generating:{chat_id}"


def _ad_enrichment_cache_key(chat_id):
    return f"misa:ads_complete:{chat_id}"


def _set_ad_enrichment_complete(chat_id, is_complete):
    if chat_id:
        cache.set(
            _ad_enrichment_cache_key(chat_id),
            bool(is_complete),
            timeout=_AD_ENRICHMENT_CACHE_TTL,
        )


def _set_chat_generating(chat_id, is_generating):
    if not chat_id:
        return
    key = _generating_cache_key(chat_id)
    if is_generating:
        cache.set(key, True, timeout=_GENERATING_CACHE_TTL)
    else:
        cache.delete(key)


def _is_chat_generating(chat_id):
    if not chat_id:
        return False
    return bool(cache.get(_generating_cache_key(chat_id)))


def _get_messages_sync(chat_id):
    return ChatService.get_messages(chat_id)


from Core_layer.Bot_package.Classes.response_utils import clean_command_response as _clean_command_response


PING_INTERVAL = 30  # секунд — keepalive для предотвращения разрыва при неактивности


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer с загрузкой истории и broadcast на все устройства."""

    def _spawn_task(self, coro, label):
        task = asyncio.create_task(coro)

        def _log_task_result(done_task):
            try:
                done_task.result()
            except asyncio.CancelledError:
                pass
            except Exception:
                logger.exception("WebSocket background task failed: %s", label)

        task.add_done_callback(_log_task_result)
        return task

    async def _safe_send_json(self, payload):
        try:
            await self.send(text_data=json.dumps(payload, ensure_ascii=False))
        except Exception:
            logger.exception("WebSocket send failed: payload_type=%s", payload.get("type"))

    async def connect(self):
        self.chat_groups = set()  # chat_id, к которым подключен
        self._ping_task = None
        await self.accept()
        await self._safe_send_json({
            'type': 'connection_established',
            'message': 'WebSocket соединение установлено'
        })
        self._ping_task = self._spawn_task(self._ping_loop(), "ping_loop")

    async def _ping_loop(self):
        """Периодическая отправка ping для keepalive (прокси, мобильные браузеры)."""
        try:
            while True:
                await asyncio.sleep(PING_INTERVAL)
                try:
                    await self._safe_send_json({'type': 'ping'})
                except Exception:
                    break
        except asyncio.CancelledError:
            pass

    async def disconnect(self, close_code):
        chat_groups = getattr(self, "chat_groups", set())
        logger.info("WebSocket disconnected: close_code=%s groups=%s", close_code, list(chat_groups))
        if self._ping_task:
            self._ping_task.cancel()
            try:
                await self._ping_task
            except asyncio.CancelledError:
                pass
        for chat_id in list(chat_groups):
            await self.channel_layer.group_discard(f"chat_{chat_id}", self.channel_name)

    async def chat_broadcast(self, event):
        """Получить broadcast от группы и отправить в WebSocket."""
        if event.get('exclude_channel') == self.channel_name:
            return
        await self._safe_send_json(event['data'])

    def _clean_command_response(self, response):
        """Убирает |command| из ответа, возвращает список частей."""
        return _clean_command_response(response)

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
                            await self._safe_send_json({
                                'type': 'history',
                                'chat_id': chat_id,
                                'messages': messages,
                                'title': title or '',
                                'isTyping': await database_sync_to_async(_is_chat_generating)(chat_id),
                            })
                            await self._send_typing_state_if_generating(chat_id)
                        return
                    if msg_type == 'join_chat':
                        chat_id = data.get('chat_id')
                        if chat_id:
                            await self._join_chat_group(chat_id)
                            await self._send_typing_state_if_generating(chat_id)
                        return
                    if msg_type == 'pong':
                        return
                    if msg_type == 'ping':
                        await self._safe_send_json({'type': 'pong'})
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
                            self._spawn_task(
                                self._process_regenerate(chat_id, message_id, user),
                                "regenerate",
                            )
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
            self._spawn_task(self._process_and_send(text_data, chat_id), "process_and_send")
        except Exception as e:
            import traceback
            logger.error(f"Error in receive: {str(e)}\n{traceback.format_exc()}")
            await self._safe_send_json({
                'type': 'error',
                'message': 'Произошла ошибка при обработке сообщения',
                'detail': str(e)
            })

    async def _broadcast_stream_event(self, chat_id, data, exclude_self=False):
        payload = {'type': 'chat_broadcast', 'data': data}
        if exclude_self:
            payload['exclude_channel'] = self.channel_name
        if chat_id:
            await self.channel_layer.group_send(f"chat_{chat_id}", payload)
        else:
            await self._safe_send_json(data)

    async def _process_and_send(self, text_data, chat_id):
        """Обрабатывает сообщение и стримит ответ — параллельно для разных чатов."""
        try:
            await self.process_message(text_data)
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
            await self._safe_send_json(err_payload)

    async def _process_regenerate(self, chat_id, message_id, user):
        """Перегенерировать ответ со стримингом; в БД пишем только финальный текст."""
        stream_id = None
        try:
            await self._join_chat_group(chat_id)
            await database_sync_to_async(_set_chat_generating)(chat_id, True)
            await self._broadcast_typing(chat_id, is_typing=True, exclude_self=True)

            def _prepare():
                msg = ChatService.get_message_by_id(chat_id, message_id)
                db_message_id = message_id
                if not msg:
                    msgs_db = ChatService.get_messages(chat_id)
                    if len(msgs_db) >= 2 and str(msgs_db[-1].get('user', '')).strip() == 'Misa':
                        db_message_id = str(msgs_db[-1]['id'])
                        msg = ChatService.get_message_by_id(chat_id, db_message_id)
                    if not msg:
                        return None, None, "Сообщение не найдено в БД (обновите чат и попробуйте снова)"
                if str(msg.get('user', '')).strip() != 'Misa':
                    return None, None, "Сообщение не от Misa"
                msgs = ChatService.get_messages(chat_id)
                idx = next((i for i, m in enumerate(msgs) if str(m['id']) == str(db_message_id)), -1)
                if idx < 1:
                    return None, None, "Нет предыдущего сообщения пользователя"
                prev = msgs[idx - 1]
                if str(prev.get('user', '')).strip() == 'Misa':
                    return None, None, "Предыдущее сообщение не от пользователя"
                user_content = str(prev.get('content', '')).strip()
                if not user_content:
                    return None, None, "Пустой запрос пользователя"
                return db_message_id, user_content, None

            db_message_id, user_content, err_msg = await database_sync_to_async(_prepare)()
            if err_msg:
                await self._safe_send_json({
                    'type': 'error',
                    'chat_id': chat_id,
                    'message': 'Ошибка перегенерации',
                    'detail': err_msg,
                })
                return

            commands = CommandAnalyzer.CommandAnalyzer('server', user_content, 'server')

            async def on_start(sid):
                nonlocal stream_id
                stream_id = sid
                await self._broadcast_stream_event(chat_id, {
                    'type': 'stream_start',
                    'chat_id': chat_id,
                    'stream_id': sid,
                    'message_id': str(db_message_id),
                    'user': 'Misa',
                    'regenerate': True,
                })

            async def on_chunk(delta, sequence):
                await self._broadcast_stream_event(chat_id, {
                    'type': 'stream_chunk',
                    'chat_id': chat_id,
                    'stream_id': stream_id,
                    'message_id': str(db_message_id),
                    'delta': delta,
                    'sequence': sequence,
                    'regenerate': True,
                })

            async def on_end(result):
                answer = str((result or {}).get('answer') or '')
                cleaned = self._clean_command_response(answer)
                msg_to_save = '\n\n'.join(cleaned) if len(cleaned) > 1 else (cleaned[0] if cleaned else answer)
                if self.is_file_path(msg_to_save):
                    msg_to_save = self.convert_file_path_to_url(msg_to_save)
                is_img = any(p.startswith('http') or p.startswith('/images/') for p in cleaned) or (
                    isinstance(msg_to_save, str) and (
                        msg_to_save.startswith('http') or msg_to_save.startswith('/images/')
                    )
                )
                await database_sync_to_async(ChatService.update_message_content)(
                    chat_id, db_message_id, msg_to_save, is_img
                )
                await self._broadcast_stream_event(chat_id, {
                    'type': 'stream_end',
                    'chat_id': chat_id,
                    'stream_id': result.get('stream_id') or stream_id,
                    'message_id': str(db_message_id),
                    'message': msg_to_save,
                    'user': 'Misa',
                    'isImage': is_img,
                    'regenerate': True,
                })
                await self.channel_layer.group_send(f"chat_{chat_id}", {
                    'type': 'chat_broadcast',
                    'data': {
                        'type': 'message_updated',
                        'chat_id': chat_id,
                        'message_id': str(db_message_id),
                        'message': msg_to_save,
                        'user': 'Misa',
                        'isImage': is_img,
                        'stream_id': result.get('stream_id') or stream_id,
                    }
                })

            async def on_error(exc):
                await self._broadcast_stream_event(chat_id, {
                    'type': 'stream_error',
                    'chat_id': chat_id,
                    'stream_id': stream_id,
                    'message_id': str(db_message_id),
                    'message': 'Ошибка перегенерации',
                    'detail': str(exc),
                    'regenerate': True,
                })

            await GenerationService.astream_tokens(
                text=user_content,
                user=user,
                chat_id=chat_id,
                pltype='server',
                commands=commands,
                should_persist=False,
                update_message_id=str(db_message_id),
                on_start=on_start,
                on_chunk=on_chunk,
                on_end=on_end,
                on_error=on_error,
            )
        except Exception as e:
            import traceback
            logger.error(f"Regenerate error: {str(e)}\n{traceback.format_exc()}")
            await self._safe_send_json({
                'type': 'error',
                'chat_id': chat_id,
                'message': 'Ошибка перегенерации',
                'detail': str(e),
            })
            if stream_id:
                await self._broadcast_stream_event(chat_id, {
                    'type': 'stream_error',
                    'chat_id': chat_id,
                    'stream_id': stream_id,
                    'message_id': str(message_id),
                    'message': 'Ошибка перегенерации',
                    'detail': str(e),
                    'regenerate': True,
                })
        finally:
            await database_sync_to_async(_set_chat_generating)(chat_id, False)
            await self._broadcast_typing(chat_id, is_typing=False, exclude_self=False)

    async def _join_chat_group(self, chat_id):
        group = f"chat_{chat_id}"
        if chat_id not in self.chat_groups:
            await self.channel_layer.group_add(group, self.channel_name)
            self.chat_groups.add(chat_id)

    async def _send_typing_state_if_generating(self, chat_id):
        """После reconnect/F5 вернуть плашку «Миса печатает», если генерация ещё идёт."""
        if await database_sync_to_async(_is_chat_generating)(chat_id):
            await self._safe_send_json({
                'type': 'typing',
                'chat_id': chat_id,
                'isTyping': True,
            })

    async def process_message(self, message):
        parts = message.split('|message|')
        if len(parts) < 2:
            return "Я не понял ваш запрос"

        if parts[1].strip() == '__NEW_CHAT__':
            return ''

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

        is_image = content.startswith('/images/') or content.startswith('http')
        if chat_id:
            user_msg_id = await database_sync_to_async(ChatService.save_message)(
                chat_id, user, content, is_image=is_image
            )
            await self._broadcast_message(
                chat_id, user, content, is_image, exclude_self=True, message_id=user_msg_id
            )
            await database_sync_to_async(_set_chat_generating)(chat_id, True)
            await self._broadcast_typing(chat_id, is_typing=True, exclude_self=True)

            # Быстрый заголовок по первому сообщению
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
                self._spawn_task(_gen_and_broadcast_title(), "generate_title_from_message")

        stream_id = None
        try:
            commands = CommandAnalyzer.CommandAnalyzer('server', content, 'server')

            async def on_start(sid):
                nonlocal stream_id
                stream_id = sid
                await self._broadcast_stream_event(chat_id, {
                    'type': 'stream_start',
                    'chat_id': chat_id,
                    'stream_id': sid,
                    'user': 'Misa',
                })

            async def on_chunk(delta, sequence):
                await self._broadcast_stream_event(chat_id, {
                    'type': 'stream_chunk',
                    'chat_id': chat_id,
                    'stream_id': stream_id,
                    'delta': delta,
                    'sequence': sequence,
                })

            async def on_end(result):
                answer = str((result or {}).get('answer') or '')
                if not answer:
                    answer = 'Я не понял ваш запрос'
                cleaned = self._clean_command_response(answer)
                msg_to_save = '\n\n'.join(cleaned) if len(cleaned) > 1 else (cleaned[0] if cleaned else answer)
                if self.is_file_path(msg_to_save):
                    msg_to_save = self.convert_file_path_to_url(msg_to_save)
                is_img = any(p.startswith('http') or p.startswith('/images/') for p in cleaned)

                pending_enrichment = GradiusService.pop_pending_enrichment(chat_id)
                await database_sync_to_async(_set_ad_enrichment_complete)(
                    chat_id, pending_enrichment is None
                )

                misa_msg_id = result.get('message_id')
                if not misa_msg_id and chat_id:
                    misa_msg_id = await database_sync_to_async(ChatService.save_message)(
                        chat_id, 'Misa', msg_to_save, is_image=is_img
                    )
                misa_msg_id = str(misa_msg_id) if misa_msg_id is not None else None

                await self._broadcast_stream_event(chat_id, {
                    'type': 'stream_end',
                    'chat_id': chat_id,
                    'stream_id': result.get('stream_id') or stream_id,
                    'message_id': misa_msg_id,
                    'message': msg_to_save,
                    'user': 'Misa',
                    'isImage': is_img,
                })
                # Совместимость со старыми клиентами + dedup через stream_id
                await self._broadcast_message(
                    chat_id,
                    'Misa',
                    msg_to_save,
                    is_img,
                    exclude_self=False,
                    message_id=misa_msg_id,
                    stream_id=result.get('stream_id') or stream_id,
                )

                if pending_enrichment is not None and misa_msg_id:
                    async def _save_complete_ad_response():
                        try:
                            final_response = await asyncio.wrap_future(pending_enrichment)
                            final_parts = self._clean_command_response(final_response)
                            final_message = (
                                '\n\n'.join(final_parts)
                                if len(final_parts) > 1
                                else (final_parts[0] if final_parts else final_response)
                            )
                            if final_message != msg_to_save:
                                final_is_img = any(
                                    part.startswith('http') or part.startswith('/images/')
                                    for part in final_parts
                                )
                                updated = await database_sync_to_async(
                                    ChatService.update_message_content
                                )(chat_id, misa_msg_id, final_message, final_is_img)
                                if updated:
                                    await self.channel_layer.group_send(
                                        f"chat_{chat_id}",
                                        {
                                            'type': 'chat_broadcast',
                                            'data': {
                                                'type': 'message_updated',
                                                'chat_id': chat_id,
                                                'message_id': str(misa_msg_id),
                                                'message': final_message,
                                                'user': 'Misa',
                                                'isImage': final_is_img,
                                            },
                                        },
                                    )
                        finally:
                            await database_sync_to_async(_set_ad_enrichment_complete)(
                                chat_id, True
                            )

                    self._spawn_task(
                        _save_complete_ad_response(),
                        "save_complete_ad_response",
                    )

                def _generate_and_save_title():
                    msgs = ChatService.get_messages(chat_id)
                    if not msgs:
                        return None
                    t = GptAnswer.GptAnswer.generate_chat_title(msgs)
                    if t and ChatService.update_title(chat_id, t):
                        return t
                    return None

                async def _generate_contextual_title():
                    title = await database_sync_to_async(_generate_and_save_title)()
                    if title:
                        await self._broadcast_title(chat_id, title)

                if chat_id:
                    self._spawn_task(
                        _generate_contextual_title(),
                        "generate_contextual_title",
                    )

            async def on_error(exc):
                await self._broadcast_stream_event(chat_id, {
                    'type': 'stream_error',
                    'chat_id': chat_id,
                    'stream_id': stream_id,
                    'message': 'Произошла ошибка при обработке сообщения',
                    'detail': str(exc),
                })

            await GenerationService.astream_tokens(
                text=content,
                user=user,
                chat_id=chat_id,
                pltype='server',
                commands=commands,
                should_persist=True,
                on_start=on_start,
                on_chunk=on_chunk,
                on_end=on_end,
                on_error=on_error,
            )
            return ''
        finally:
            if chat_id:
                await database_sync_to_async(_set_chat_generating)(chat_id, False)
                await self._broadcast_typing(chat_id, is_typing=False, exclude_self=False)

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

    async def _broadcast_message(
        self,
        chat_id,
        user,
        content,
        is_image=False,
        exclude_self=False,
        message_id=None,
        stream_id=None,
    ):
        """Отправить сообщение всем подключённым к чату (все устройства)."""
        data = {
            'type': 'chat_message',
            'chat_id': chat_id,
            'message': content,
            'user': user,
            'isImage': is_image,
        }
        if message_id is not None:
            data['message_id'] = str(message_id)
        if stream_id is not None:
            data['stream_id'] = str(stream_id)
        payload = {
            'type': 'chat_broadcast',
            'data': data,
        }
        if exclude_self:
            payload['exclude_channel'] = self.channel_name
        if chat_id:
            await self.channel_layer.group_send(f"chat_{chat_id}", payload)
        else:
            await self._safe_send_json(data)

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