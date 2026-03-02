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

# SMTP для отправки кодов верификации (maildev в docker)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('SMTP_HOST', 'smtp-service-misa')
EMAIL_PORT = int(os.getenv('SMTP_PORT', 1025))
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
# Отображаемое имя отправителя: Misa <mailer7012@gmail.com>
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Misa <mailer7012@gmail.com>')

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    # Ваш кастомный middleware из Core_layer
    'Core_layer.Middleware_package.Classes.Middleware.Middleware',
]