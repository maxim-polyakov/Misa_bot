INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels'
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