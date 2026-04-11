from django.urls import path, re_path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from . import views
import os


def home_view(request):
    return HttpResponse("Django server is working!")


urlpatterns = [
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('og/preview/', views.spa_og_preview, name='spa_og_preview'),
    # HTML + Open Graph для превью ссылок (Telegram и др.); со слэшем и без
    re_path(r'^share/(?P<chat_id>[^/]+)/?$', views.share_chat_html, name='share_chat_html'),
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
    path('auth/google-id-token/', views.google_id_token, name='google_id_token'),
    path('auth/check/', views.check, name="check"),
    path('auth/logout-all/', views.logout_all, name='logout_all'),
    path('auth/delete-account/', views.delete_account, name='delete_account'),
    # OpenAPI 3 + Swagger UI / ReDoc (drf-spectacular)
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui-alt'),
    path('swagger-ui/index.html', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui-html'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='schema-redoc'),
    path('swagger.json', SpectacularAPIView.as_view(), name='schema-json'),
    # Chat API (хранение в БД)
    path('api/ui-locale/', views.ui_locale, name='ui_locale'),
    path('api/chats/', views.chats_list_or_create, name='chats_list_or_create'),
    path('api/chats/export/', views.chats_export, name='chats_export'),
    path('api/chats/<str:chat_id>/share/', views.chats_share_public, name='chats_share_public'),
    path('api/chats/<str:chat_id>/messages/', views.chats_messages, name='chats_messages'),
    path('api/chats/<str:chat_id>/messages/<str:message_id>/feedback/', views.chats_message_feedback, name='chats_message_feedback'),
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
