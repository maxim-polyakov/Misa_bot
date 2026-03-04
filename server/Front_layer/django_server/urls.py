from django.urls import path, re_path
from django.http import HttpResponse
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


def swagger_ui_view(request):
    """Swagger UI через CDN — без DRF, без Django Login."""
    schema_url = request.build_absolute_uri('/swagger.json')
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
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
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