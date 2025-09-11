import nltk
import os
import sys
import django
import asyncio
from Front_layer.django_server.asgi import application
from hypercorn.asyncio import serve
from hypercorn.config import Config



# ______________________________________________________________________________

if __name__ == "__main__":
    nltk.download('stopwords')
    # Устанавливаем настройки Django с правильным путем
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Front_layer.django_server.settings')
    # Инициализируем Django
    django.setup()

    # Используем InMemoryChannelLayer вместо Redis
    print("Используется InMemoryChannelLayer (без Redis)")

    # Запускаем ASGI сервер напрямую
    print("Запуск Django ASGI сервера...")

    # Конфигурация Hypercorn
    config = Config()
    config.bind = ["0.0.0.0:8001"]

    # Запускаем сервер
    asyncio.run(serve(application, config))