from django.urls import path, re_path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from Core_layer.Middleware_package.Classes import Middleware
from . import views
import os


def home_view(request):
    return HttpResponse("Django server is working!")

# Применяем middleware к конкретному view


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