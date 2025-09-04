import nltk
import os
import sys
import django
import asyncio
from django.core.asgi import get_asgi_application
from Front_layer.django_server.asgi import application
from hypercorn.asyncio import serve
from hypercorn.config import Config

# Добавляем путь к проекту в sys.path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Импортируем ваш модуль
import Front_layer.django_server as dj
from Core_layer.Test_package.Classes.PythonTests import TestRun as PyTest

# ______________________________________________________________________________

if __name__ == "__main__":
    # Устанавливаем настройки Django с правильным путем
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Front_layer.django_server.settings')

    # Добавляем путь к папке Front_layer в Python path
    front_layer_path = os.path.join(project_path, 'Front_layer')
    sys.path.append(front_layer_path)

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