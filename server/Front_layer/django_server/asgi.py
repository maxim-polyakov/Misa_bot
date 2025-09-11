import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import routing  # Импортируйте вашу маршрутизацию

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Front_layer.django_server.settings')

# Базовое ASGI-приложение для HTTP
django_asgi_app = get_asgi_application()

# Полное ASGI-приложение с поддержкой WebSocket
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})