# chat/consumers.py
import json
import logging
import os
from urllib.parse import quote
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorServer

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'WebSocket соединение установлено'
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            response = await self.process_message(text_data)
            outarr = response.split('\n')
            outarr = [word for word in outarr if word !='']
            for el in outarr:
                if self.is_file_path(el):
                    el =  self.convert_file_path_to_url(el)

                await self.send(text_data=json.dumps({
                    'type': 'chat_message',
                    'message': el,
                    'user': 'Misa'
                }, ensure_ascii=False))



        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Произошла ошибка при обработке сообщения'
            }, ensure_ascii=False))

    async def process_message(self, message):
        message_monitor = MessageMonitorServer.MessageMonitorServer(message=message)
        response = message_monitor.monitor()

        if not response:
            return "Я не понял ваш запрос"

        return response

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