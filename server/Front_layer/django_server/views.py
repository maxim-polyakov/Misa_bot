import re
from html import escape as html_escape
from urllib.parse import quote

from django.conf import settings
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from Core_layer.Controller_package.Classes import Controller
from . import openapi_examples as oex

_BEARER = [{'bearerAuth': []}]


# Контроллер регистрации
@extend_schema(
    summary='Регистрация (legacy)',
    tags=['Auth'],
    request=oex.REQ_EMAIL_PASSWORD,
    examples=[oex.EX_EMAIL_PASSWORD],
    responses={201: oex.RESP_AUTH_TOKEN_USER},
)
@api_view(['POST'])
@csrf_exempt
def register(request):
    """Регистрация нового пользователя (legacy, без верификации)"""
    ctrlr = Controller.Controller()
    return ctrlr.register(request)


@extend_schema(
    summary='Отправка кода верификации',
    tags=['Auth'],
    request=oex.REQ_EMAIL_PASSWORD,
    examples=[oex.EX_EMAIL_PASSWORD],
    responses={200: oex.RESP_AUTH_EMAIL_SENT},
)
@api_view(['POST'])
@csrf_exempt
def register_send_code(request):
    """Отправка кода верификации на email"""
    ctrlr = Controller.Controller()
    return ctrlr.register_send_code(request)


@extend_schema(
    summary='Проверка кода и создание пользователя',
    tags=['Auth'],
    request=oex.REQ_REGISTER_VERIFY,
    examples=[oex.EX_REGISTER_VERIFY],
    responses={201: oex.RESP_AUTH_TOKEN_USER},
)
@api_view(['POST'])
@csrf_exempt
def register_verify(request):
    """Проверка кода и создание пользователя"""
    ctrlr = Controller.Controller()
    return ctrlr.register_verify(request)


@extend_schema(
    summary='Отправка кода восстановления пароля',
    tags=['Auth'],
    request=oex.REQ_EMAIL_ONLY,
    examples=[oex.EX_EMAIL_ONLY],
    responses={200: oex.RESP_AUTH_EMAIL_SENT},
)
@api_view(['POST'])
@csrf_exempt
def forgot_password_send_code(request):
    """Отправка кода восстановления пароля на email"""
    ctrlr = Controller.Controller()
    return ctrlr.forgot_password_send_code(request)


@extend_schema(
    summary='Проверка кода и установка нового пароля',
    tags=['Auth'],
    request=oex.REQ_FORGOT_VERIFY,
    examples=[oex.EX_FORGOT_VERIFY],
    responses={200: oex.RESP_AUTH_TOKEN_USER},
)
@api_view(['POST'])
@csrf_exempt
def forgot_password_verify(request):
    """Проверка кода и установка нового пароля"""
    ctrlr = Controller.Controller()
    return ctrlr.forgot_password_verify(request)


# Контроллер авторизации
@extend_schema(
    summary='Вход по email/паролю',
    tags=['Auth'],
    request=oex.REQ_EMAIL_PASSWORD,
    examples=[oex.EX_EMAIL_PASSWORD],
    responses={200: oex.RESP_LOGIN},
)
@api_view(['POST'])
@csrf_exempt
def login_view(request):
    ctrlr = Controller.Controller()
    return ctrlr.login_view(request)


# Google OAuth
@extend_schema(
    summary='OAuth Google redirect',
    tags=['Auth'],
    parameters=[oex.PARAM_REDIRECT_URI],
)
@api_view(['GET'])
@csrf_exempt
def oauth_google_redirect(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_redirect(request)


@extend_schema(
    summary='OAuth Google callback',
    tags=['Auth'],
    parameters=oex.PARAM_GOOGLE_CALLBACK,
)
@api_view(['GET'])
@csrf_exempt
def oauth_google_callback(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_callback(request)


@extend_schema(
    summary='OAuth token',
    tags=['Auth'],
    parameters=[oex.PARAM_OAUTH_CODE],
    responses={200: oex.RESP_OAUTH_TOKEN},
)
@api_view(['GET'])
@csrf_exempt
def oauth_token(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_token(request)


@extend_schema(
    summary='Google ID token (Android)',
    tags=['Auth'],
    request=oex.REQ_GOOGLE_ID_TOKEN,
    examples=[oex.EX_GOOGLE_ID_TOKEN],
    responses={200: oex.RESP_AUTH_TOKEN_USER},
)
@api_view(['POST'])
@csrf_exempt
def google_id_token(request):
    ctrlr = Controller.Controller()
    return ctrlr.google_id_token(request)


@extend_schema(
    summary='Проверка JWT',
    tags=['Auth'],
    auth=_BEARER,
    responses={200: oex.RESP_CHECK},
)
@api_view(['GET'])
@csrf_exempt
def check(request):
    ctrlr = Controller.Controller()
    return ctrlr.check(request)


@extend_schema(
    summary='Выход со всех устройств',
    tags=['Auth'],
    auth=_BEARER,
    request=oex.REQ_EMPTY_OBJECT,
    examples=[oex.EX_EMPTY_OBJECT],
    responses={200: oex.RESP_EMPTY_OK},
)
@api_view(['POST'])
@csrf_exempt
def logout_all(request):
    """Выход со всех устройств"""
    ctrlr = Controller.Controller()
    return ctrlr.logout_all(request)


@extend_schema(
    summary='Удаление аккаунта',
    tags=['Auth'],
    auth=_BEARER,
    request=oex.REQ_EMPTY_OBJECT,
    examples=[oex.EX_EMPTY_OBJECT],
    responses={200: oex.RESP_EMPTY_OK},
)
@api_view(['POST'])
@csrf_exempt
def delete_account(request):
    """Удаление аккаунта пользователя (необратимо)"""
    ctrlr = Controller.Controller()
    return ctrlr.delete_account(request)


# Chat API (требует JWT)
@extend_schema(
    summary='Список чатов',
    tags=['Chats'],
    auth=_BEARER,
    methods=['GET'],
    responses={200: oex.RESP_CHATS_LIST},
)
@extend_schema(
    summary='Создать чат',
    tags=['Chats'],
    auth=_BEARER,
    methods=['POST'],
    request=oex.REQ_CHAT_CREATE,
    examples=[oex.EX_CHAT_CREATE],
    responses={201: oex.RESP_CHAT_CREATE},
)
@api_view(['GET', 'POST'])
@csrf_exempt
def chats_list_or_create(request):
    ctrlr = Controller.Controller()
    if request.method == "GET":
        return ctrlr.chats_list(request)
    return ctrlr.chats_create(request)


@extend_schema(
    summary='Экспорт чатов',
    tags=['Chats'],
    auth=_BEARER,
    responses={200: oex.RESP_CHATS_EXPORT},
)
@api_view(['GET'])
def chats_export(request):
    ctrlr = Controller.Controller()
    return ctrlr.chats_export(request)


def _share_description_for_og(messages, max_len=220):
    """Краткий текст для og:description (первое содержательное сообщение)."""
    for m in messages or []:
        c = m.get('content') or ''
        if not str(c).strip():
            continue
        text = re.sub(r'```[\s\S]*?```', '', str(c))
        text = re.sub(r'\s+', ' ', text).strip()
        if not text:
            continue
        if len(text) > max_len:
            text = text[: max_len - 1] + '…'
        return text
    return 'Misa AI — чат с искусственным интеллектом'


@csrf_exempt
def share_chat_html(request, chat_id):
    """
    HTML с Open Graph для /share/<chat_id>/ — для краулеров (Telegram и др.).
    Пользователи открывают тот же URL в браузере и получают SPA с фронта.
    """
    ctrlr = Controller.Controller()
    try:
        payload = ctrlr.get_share_chat_payload(request, chat_id)
    except Exception:
        raise Http404('Chat not found')
    if payload is None:
        raise Http404('Chat not found')

    title = payload.get('title') or 'Чат'
    messages = payload.get('messages') or []
    site_base = getattr(settings, 'WEB_APP_PUBLIC_URL', '').rstrip('/')
    og_desc = _share_description_for_og(messages)
    og_title = html_escape(f'{title} | Misa AI')
    og_desc_esc = html_escape(og_desc)

    og_url = f'{site_base}/share/{quote(str(chat_id), safe="")}'
    msg_q = request.GET.get('msg')
    if msg_q:
        og_url += f'?msg={quote(msg_q, safe="")}'

    og_image = f'{site_base}/favicon-195.png' if site_base else ''
    og_image_esc = html_escape(og_image) if og_image else ''

    parts = [
        '<!DOCTYPE html>',
        '<html lang="ru">',
        '<head>',
        '<meta charset="utf-8" />',
        '<meta name="viewport" content="width=device-width, initial-scale=1" />',
        f'<meta name="description" content="{og_desc_esc}" />',
        f'<meta property="og:title" content="{og_title}" />',
        f'<meta property="og:description" content="{og_desc_esc}" />',
        f'<meta property="og:url" content="{html_escape(og_url)}" />',
        '<meta property="og:type" content="website" />',
        '<meta property="og:site_name" content="Misa AI" />',
    ]
    if og_image:
        parts.append(f'<meta property="og:image" content="{og_image_esc}" />')
        parts.append(f'<meta property="og:image:alt" content="{og_title}" />')
    parts.extend([
        '<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{og_title}" />',
        f'<meta name="twitter:description" content="{og_desc_esc}" />',
    ])
    if og_image:
        parts.append(f'<meta name="twitter:image" content="{og_image_esc}" />')
    parts.extend([
        f'<link rel="canonical" href="{html_escape(og_url)}" />',
        f'<title>{og_title}</title>',
        '</head>',
        '<body>',
        f'<p><a href="{html_escape(og_url)}">Открыть чат в Misa AI</a></p>',
        '</body>',
        '</html>',
    ])
    return HttpResponse('\n'.join(parts), content_type='text/html; charset=utf-8')


@extend_schema(
    summary='Публичный просмотр чата (без авторизации)',
    tags=['Chats'],
    parameters=[oex.PARAM_CHAT_ID, oex.PARAM_SHARE_MSG],
    responses={200: oex.RESP_SHARE_PUBLIC},
)
@api_view(['GET'])
@csrf_exempt
def chats_share_public(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_share_public(request, chat_id)


@extend_schema(
    summary='Сообщения чата',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID],
    responses={200: oex.RESP_CHAT_MESSAGES},
)
@api_view(['GET'])
def chats_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_messages(request, chat_id)


@extend_schema(
    summary='Лайк/дизлайк сообщения',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID, oex.PARAM_MESSAGE_ID],
    request=oex.REQ_MESSAGE_FEEDBACK,
    examples=[oex.EX_MESSAGE_FEEDBACK],
    responses={200: oex.RESP_MESSAGE_FEEDBACK},
)
@api_view(['PATCH'])
@csrf_exempt
def chats_message_feedback(request, chat_id, message_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_message_feedback(request, chat_id, message_id)


@extend_schema(
    summary='Очистить сообщения чата',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID],
    responses={200: oex.RESP_EMPTY_OK},
)
@api_view(['DELETE'])
@csrf_exempt
def chats_clear_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_clear_messages(request, chat_id)


@extend_schema(
    summary='Обновить чат',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID],
    request=oex.REQ_CHAT_TITLE,
    examples=[oex.EX_CHAT_TITLE],
    responses={200: oex.RESP_CHAT_UPDATE},
)
@api_view(['PATCH'])
@csrf_exempt
def chats_update(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_update_title(request, chat_id)


@extend_schema(
    summary='Удалить чат',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID],
    responses={200: oex.RESP_EMPTY_OK},
)
@api_view(['DELETE'])
@csrf_exempt
def chats_delete(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_delete(request, chat_id)
