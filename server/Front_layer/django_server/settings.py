import os
from pathlib import Path

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels'
]

# API URL из переменных окружения
API_URL = os.getenv('API_URL', '')

# Предполагаем, что BASE_DIR это корень проекта (где manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Или подстройте под вашу структуру

# URL для доступа к статическим файлам
STATIC_URL = '/'

# Директории, где Django ищет статические файлы, кроме app/static/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'images'),  # Укажите путь к вашей папке images
]

ROOT_URLCONF = 'Front_layer.django_server.urls'
ASGI_APPLICATION = 'Front_layer.django_server.asgi.application'
ALLOWED_HOSTS = ['*']
# Замените Redis на InMemoryChannelLayer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
MIDDLEWARE = [

    # Ваш кастомный middleware из Core_layer
    'Core_layer.Middleware_package.Classes.Middleware.Middleware',
]