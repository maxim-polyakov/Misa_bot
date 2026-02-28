import os
from pathlib import Path

from dotenv import load_dotenv

# Загружаем переменные из .env (приоритет над environment)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env', override=True)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'channels'
]

# API URL из .env
API_URL = os.getenv('API_URL', '')

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
CORS_ALLOW_ALL_ORIGINS = True
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    # Ваш кастомный middleware из Core_layer
    'Core_layer.Middleware_package.Classes.Middleware.Middleware',
]