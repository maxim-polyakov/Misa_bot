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
    'channels',
    'rest_framework',
    'drf_spectacular',
]

# API URL из .env
API_URL = os.getenv('API_URL', '')
# Публичный URL веб-клиента (Open Graph, редирект /share/<id>/ → SPA)
WEB_APP_PUBLIC_URL = (
    os.getenv('WEB_APP_PUBLIC_URL') or os.getenv('FRONTEND_URL') or 'https://misa.baxic.ru'
).rstrip('/')

# SECRET_KEY обязателен для Django (сессии, CSRF, шаблоны)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# DEBUG: при True показывает полный traceback на странице (для отладки 500)
# В .env: DEBUG=1 или DEBUG=true. После отладки отключить!
DEBUG = os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes')

# Шаблоны (Swagger UI из drf-spectacular)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

# URL для доступа к статическим файлам
STATIC_URL = '/static/'

# MEDIA_URL должен отличаться от STATIC_URL (требование Django)
MEDIA_URL = '/media/'

# Директории, где Django ищет статические файлы, кроме app/static/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'images'),  # Укажите путь к вашей папке images
]

ROOT_URLCONF = 'Front_layer.django_server.urls'
ASGI_APPLICATION = 'Front_layer.django_server.asgi.application'
ALLOWED_HOSTS = ['*']
# Channel layers и кэш: Redis если задан REDIS_URL
REDIS_URL = os.getenv('REDIS_URL', '')
if REDIS_URL:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {'hosts': [REDIS_URL]},
        },
    }
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
        },
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
    }
CORS_ALLOW_ALL_ORIGINS = True
# Разрешённые клиенты: web (client/), android (android/)
ALLOWED_CLIENTS = ['web', 'android']

# REST Framework: отключаем SessionAuthentication по умолчанию для API
# (иначе Swagger и другие API показывают Django Login)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# OpenAPI 3 (drf-spectacular)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Misa API',
    'VERSION': '1.0.0',
    'DESCRIPTION': (
        'API Misa Bot.\n\n'
        '**Try it out:** для защищённых методов нажмите **Authorize**, вставьте JWT '
        '(поле `data.token` после `POST /auth/login/` или новый токен из `GET /auth/check/`). '
        'Префикс `Bearer ` Swagger подставит сам.\n\n'
        'В телах запросов и в параметрах пути уже есть примеры значений.'
    ),
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'displayRequestDuration': True,
    },
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'bearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'JWT из ответа POST /auth/login/ (поле data.token)',
            }
        }
    },
}

# Yandex Object Storage (S3-совместимый) для изображений
S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', '')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', '')
S3_BUCKET = os.getenv('S3_BUCKET', '')

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