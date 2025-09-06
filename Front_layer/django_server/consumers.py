# chat/consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorServer

# Настройка логирования
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_handler = None  # Замените на ваш класс команд

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
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Обрабатываем сообщение через ваш MessageMonitor
            response = await self.process_message(message)

            # Отправляем ответ в правильном формате
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': response,
                'user': 'Misa'
            }, ensure_ascii=False))  # Важно: ensure_ascii=False

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Произошла ошибка при обработке сообщения'
            }))

    async def process_message(self, message):
        message_monitor = MessageMonitorServer.MessageMonitorServer(message=message)
        response = message_monitor.monitor()

        return response if response else "Я не понял ваш запрос"