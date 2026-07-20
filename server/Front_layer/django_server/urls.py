from django.urls import include, re_path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from dmr.openapi import OpenAPIConfig, build_schema
from dmr.openapi.views import OpenAPIJsonView, RedocView, SwaggerView
from dmr.routing import Router, path
from . import dmr_views, views
import os


def home_view(request):
    return HttpResponse("Django server is working!")


api_router = Router(
    '',
    [
        # Аутентификация
        path('auth/register/', dmr_views.RegisterController.as_view(), name='register'),
        path('auth/register/send-code/', dmr_views.RegisterSendCodeController.as_view(), name='register_send_code'),
        path('auth/register/verify/', dmr_views.RegisterVerifyController.as_view(), name='register_verify'),
        path('auth/forgot-password/send-code/', dmr_views.ForgotPasswordSendCodeController.as_view(), name='forgot_password_send_code'),
        path('auth/forgot-password/verify/', dmr_views.ForgotPasswordVerifyController.as_view(), name='forgot_password_verify'),
        path('auth/login/', dmr_views.LoginController.as_view(), name='login'),
        path('auth/oauth-token/', dmr_views.OAuthTokenController.as_view(), name='oauth_token'),
        path('auth/google-id-token/', dmr_views.GoogleIdTokenController.as_view(), name='google_id_token'),
        path('auth/check/', dmr_views.CheckController.as_view(), name='check'),
        path('auth/logout-all/', dmr_views.LogoutAllController.as_view(), name='logout_all'),
        path('auth/delete-account/', dmr_views.DeleteAccountController.as_view(), name='delete_account'),
        # Chat API (хранение в БД через DB_Communication/pandas)
        path('api/ui-locale/', dmr_views.UiLocaleController.as_view(), name='ui_locale'),
        path('api/chats/', dmr_views.ChatsController.as_view(), name='chats_list_or_create'),
        path('api/chats/export/', dmr_views.ChatsExportController.as_view(), name='chats_export'),
        path('api/chats/<str:chat_id>/share/', dmr_views.ChatSharePublicController.as_view(), name='chats_share_public'),
        path('api/chats/<str:chat_id>/messages/', dmr_views.ChatMessagesController.as_view(), name='chats_messages'),
        path('api/chats/<str:chat_id>/messages/<str:message_id>/feedback/', dmr_views.ChatMessageFeedbackController.as_view(), name='chats_message_feedback'),
        path('api/chats/<str:chat_id>/messages/clear/', dmr_views.ChatClearMessagesController.as_view(), name='chats_clear_messages'),
        path('api/chats/<str:chat_id>/', dmr_views.ChatUpdateController.as_view(), name='chats_update'),
        path('api/chats/<str:chat_id>/delete/', dmr_views.ChatDeleteController.as_view(), name='chats_delete'),
    ],
)
openapi_schema = build_schema(
    api_router,
    config=OpenAPIConfig(
        title='Misa API',
        version='1.0.0',
        description=(
            'API Misa Bot. Защищённые методы используют JWT из ответа '
            'POST /auth/login/ или GET /auth/check/ в заголовке Authorization.'
        ),
    ),
)

urlpatterns = [
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('og/preview/', views.spa_og_preview, name='spa_og_preview'),
    # HTML + Open Graph для превью ссылок (Telegram и др.); со слэшем и без
    re_path(r'^share/(?P<chat_id>[^/]+)/?$', views.share_chat_html, name='share_chat_html'),
    path('', home_view),
    path(api_router.prefix, include((api_router.urls, 'misa_api'), namespace='api')),
    # Google OAuth endpoints with browser/custom-scheme redirects stay as regular Django views.
    path('auth/oauth/google/', views.oauth_google_redirect, name='oauth_google_redirect'),
    path('auth/oauth/callback', views.oauth_google_callback, name='oauth_google_callback'),
    # OpenAPI 3 + Swagger UI / ReDoc (django-modern-rest)
    path('schema/', OpenAPIJsonView.as_view(openapi_schema), name='schema'),
    path('swagger.json', OpenAPIJsonView.as_view(openapi_schema), name='schema-json'),
    path('swagger/', SwaggerView.as_view(openapi_schema), name='schema-swagger-ui'),
    path('swagger-ui/', SwaggerView.as_view(openapi_schema), name='schema-swagger-ui-alt'),
    path('swagger-ui/index.html', SwaggerView.as_view(openapi_schema), name='schema-swagger-ui-html'),
    path('redoc/', RedocView.as_view(openapi_schema), name='schema-redoc'),
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
