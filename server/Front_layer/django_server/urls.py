from django.urls import path, re_path
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from Core_layer.Middleware_package.Classes import Middleware
from . import views
import os


def home_view(request):
    return HttpResponse("Django server is working!")


def swagger_json_view(request):
    """OpenAPI 2.0 схема с BaseURL и всеми эндпоинтами."""
    base_url = getattr(settings, 'API_URL', '').rstrip('/').replace('https://', '').replace('http://', '')
    host = base_url or request.get_host()
    scheme = 'https' if 'https' in str(getattr(settings, 'API_URL', '')) else 'http'

    schema = {
        "swagger": "2.0",
        "info": {"title": "Misa API", "version": "v1", "description": "API документация Misa Bot"},
        "host": host,
        "basePath": "/",
        "schemes": [scheme],
        "paths": {
            "/auth/register/": {"post": {"summary": "Регистрация (legacy)", "tags": ["Auth"]}},
            "/auth/register/send-code/": {"post": {"summary": "Отправить код верификации", "tags": ["Auth"], "parameters": [{"name": "body", "in": "body", "schema": {"type": "object", "properties": {"email": {}, "password": {}}}}]}},
            "/auth/register/verify/": {"post": {"summary": "Подтвердить код", "tags": ["Auth"], "parameters": [{"name": "body", "in": "body", "schema": {"type": "object", "properties": {"email": {}, "password": {}, "code": {}}}}]}},
            "/auth/forgot-password/send-code/": {"post": {"summary": "Код восстановления пароля", "tags": ["Auth"], "parameters": [{"name": "body", "in": "body", "schema": {"type": "object", "properties": {"email": {}}}}]}},
            "/auth/forgot-password/verify/": {"post": {"summary": "Сбросить пароль по коду", "tags": ["Auth"], "parameters": [{"name": "body", "in": "body", "schema": {"type": "object", "properties": {"email": {}, "code": {}, "new_password": {}}}}]}},
            "/auth/login/": {"post": {"summary": "Вход", "tags": ["Auth"], "parameters": [{"name": "body", "in": "body", "schema": {"type": "object", "properties": {"email": {}, "password": {}}}}]}},
            "/auth/check/": {"get": {"summary": "Проверка JWT", "tags": ["Auth"], "security": [{"Bearer": []}]}},
            "/auth/logout-all/": {"post": {"summary": "Выход со всех устройств", "tags": ["Auth"], "security": [{"Bearer": []}]}},
            "/api/chats/": {"get": {"summary": "Список чатов", "tags": ["Chats"], "security": [{"Bearer": []}]}, "post": {"summary": "Создать чат", "tags": ["Chats"], "security": [{"Bearer": []}]}},
            "/api/chats/export/": {"get": {"summary": "Экспорт чатов", "tags": ["Chats"], "security": [{"Bearer": []}]}},
            "/api/chats/{chat_id}/": {"patch": {"summary": "Обновить чат", "tags": ["Chats"], "security": [{"Bearer": []}]}},
            "/api/chats/{chat_id}/delete/": {"delete": {"summary": "Удалить чат", "tags": ["Chats"], "security": [{"Bearer": []}]}},
            "/api/chats/{chat_id}/messages/": {"get": {"summary": "Сообщения чата", "tags": ["Chats"], "security": [{"Bearer": []}]}},
            "/api/chats/{chat_id}/messages/clear/": {"delete": {"summary": "Очистить сообщения", "tags": ["Chats"], "security": [{"Bearer": []}]}},
        },
        "securityDefinitions": {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}},
    }
    return JsonResponse(schema)


def swagger_ui_view(request):
    """Swagger UI через CDN — без DRF, без Django Login."""
    schema_url = '/swagger.json'
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Misa API - Swagger</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({{
            url: "{schema_url}",
            dom_id: "#swagger-ui",
            layout: "BaseLayout",
            docExpansion: "list",
            filter: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ]
        }});
    </script>
</body>
</html>'''
    return HttpResponse(html, content_type='text/html')


# URL-паттерны только для схемы (без catch-all и static)
api_patterns_for_schema = [
    path('auth/register/', views.register, name='register'),
    path('auth/register/send-code/', views.register_send_code, name='register_send_code'),
    path('auth/register/verify/', views.register_verify, name='register_verify'),
    path('auth/forgot-password/send-code/', views.forgot_password_send_code, name='forgot_password_send_code'),
    path('auth/forgot-password/verify/', views.forgot_password_verify, name='forgot_password_verify'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/oauth/google/', views.oauth_google_redirect, name='oauth_google_redirect'),
    path('auth/oauth/callback', views.oauth_google_callback, name='oauth_google_callback'),
    path('auth/oauth-token/', views.oauth_token, name='oauth_token'),
    path('auth/check/', views.check, name='check'),
    path('auth/logout-all/', views.logout_all, name='logout_all'),
    path('api/chats/', views.chats_list_or_create, name='chats_list_or_create'),
    path('api/chats/export/', views.chats_export, name='chats_export'),
    path('api/chats/<str:chat_id>/messages/', views.chats_messages, name='chats_messages'),
    path('api/chats/<str:chat_id>/messages/clear/', views.chats_clear_messages, name='chats_clear_messages'),
    path('api/chats/<str:chat_id>/', views.chats_update, name='chats_update'),
    path('api/chats/<str:chat_id>/delete/', views.chats_delete, name='chats_delete'),
]

# Swagger / OpenAPI (без аутентификации — иначе DRF показывает Django Login)
schema_view = get_schema_view(
    openapi.Info(
        title="Misa API",
        default_version="v1",
        description="API документация Misa Bot",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],  # отключаем SessionAuthentication — иначе редирект на login
    patterns=api_patterns_for_schema,
)

urlpatterns = [
    # Аутентификация
    path('', home_view),
    path('auth/register/', views.register, name='register'),
    path('auth/register/send-code/', views.register_send_code, name='register_send_code'),
    path('auth/register/verify/', views.register_verify, name='register_verify'),
    path('auth/forgot-password/send-code/', views.forgot_password_send_code, name='forgot_password_send_code'),
    path('auth/forgot-password/verify/', views.forgot_password_verify, name='forgot_password_verify'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/oauth/google/', views.oauth_google_redirect, name='oauth_google_redirect'),
    path('auth/oauth/callback', views.oauth_google_callback, name='oauth_google_callback'),
    path('auth/oauth-token/', views.oauth_token, name='oauth_token'),
    path('auth/check/', views.check, name="check"),
    path('auth/logout-all/', views.logout_all, name='logout_all'),
    # Swagger UI (своя страница через CDN — без DRF/Django Login)
    path('swagger-ui/', swagger_ui_view, name='schema-swagger-ui'),
    path('swagger-ui/index.html', swagger_ui_view, name='schema-swagger-ui-html'),
    path('swagger/', swagger_ui_view, name='schema-swagger-legacy'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', swagger_json_view, name='schema-json'),
    # Chat API (хранение в БД)
    path('api/chats/', views.chats_list_or_create, name='chats_list_or_create'),
    path('api/chats/export/', views.chats_export, name='chats_export'),
    path('api/chats/<str:chat_id>/messages/', views.chats_messages, name='chats_messages'),
    path('api/chats/<str:chat_id>/messages/clear/', views.chats_clear_messages, name='chats_clear_messages'),
    path('api/chats/<str:chat_id>/', views.chats_update, name='chats_update'),
    path('api/chats/<str:chat_id>/delete/', views.chats_delete, name='chats_delete'),
]

# Для production: обслуживание статических файлов через Django (не рекомендуется для высоконагруженных проектов)
if not settings.DEBUG:
    # Явно обслуживаем папку images
    urlpatterns += [
        re_path(r'^images/(?P<path>.*)$', serve, {
            'document_root': os.path.join(settings.BASE_DIR, 'images'),
        }),
    ]

    # Обслуживаем другие статические директории
    for static_dir in settings.STATICFILES_DIRS:
        urlpatterns += [
            re_path(r'^(?P<path>.*)$', serve, {
                'document_root': static_dir,
            }),
        ]

    # Fallback для любых файлов в корне проекта
    urlpatterns += [
        re_path(r'^(?P<path>.*)$', serve, {
            'document_root': settings.BASE_DIR,
        }),
    ]
else:
    # Для development
    urlpatterns += static(
        '/images/',
        document_root=os.path.join(settings.BASE_DIR, 'images')
    )

    for static_dir in settings.STATICFILES_DIRS:
        urlpatterns += static(
            settings.STATIC_URL,
            document_root=static_dir,
            show_indexes=True
        )