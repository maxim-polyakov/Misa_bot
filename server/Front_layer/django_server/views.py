import json
import os
import re
import struct
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

# Старая заглушка Pillow ~2KB; нормальный арт (misa.png) — сотни KB.
_OG_LOCAL_IMAGE_MIN_BYTES = 8000
# client/public/misa.png (если на сервере нет og_share.png для чтения IHDR)
_MISA_PNG_FALLBACK_WH = (800, 1120)


def _png_ihdr_dimensions(path):
    """Ширина/высота PNG без Pillow (для og:image:width/height — Telegram рекомендует meta)."""
    try:
        with open(path, 'rb') as f:
            if f.read(8) != b'\x89PNG\r\n\x1a\n':
                return None, None
            length = struct.unpack('>I', f.read(4))[0]
            if f.read(4) != b'IHDR':
                return None, None
            data = f.read(length)
            w, h = struct.unpack('>II', data[:8])
            return w, h
    except (OSError, struct.error):
        return None, None


def _og_share_image_dimensions(og_image_url):
    if not og_image_url:
        return None, None
    img_dir = os.path.join(settings.BASE_DIR, 'images')
    for name in ('og_share.png', 'misaimg.png'):
        if name in og_image_url:
            p = os.path.join(img_dir, name)
            if os.path.isfile(p):
                return _png_ihdr_dimensions(p)
    if og_image_url.rstrip('/').lower().endswith('misa.png'):
        p = os.path.join(img_dir, 'og_share.png')
        if os.path.isfile(p):
            return _png_ihdr_dimensions(p)
        return _MISA_PNG_FALLBACK_WH
    return None, None


def _share_should_redirect_to_spa(request):
    """
    Редирект location.replace() только для обычного браузера по ссылке.
    Краулеры Telegram и др. часто без Sec-Fetch-Mode или с другим UA — им нельзя вставлять script:
    иначе превью в Telegram может не собираться.
    """
    ua = (request.META.get('HTTP_USER_AGENT') or '').lower()
    if any(
        x in ua
        for x in (
            'telegram',
            'twitterbot',
            'facebookexternalhit',
            'whatsapp',
            'linkedinbot',
            'slackbot',
            'discordbot',
            'vkshare',
            'pinterestbot',
            'skypeuripreview',
            'embedly',
            'googlebot',
            'bingbot',
            'yandexbot',
            'bytespider',
        )
    ):
        return False
    # Только настоящий переход по ссылке в Chrome/Safari/Firefox (у Telegram-краулера Sec-Fetch нет).
    # Раньше был fallback по «mozilla без bot» — лишний <script> мог мешать превью в Telegram.
    return request.META.get('HTTP_SEC_FETCH_MODE') == 'navigate'


def _share_og_absolute_api_url(request, path):
    """Абсолютный URL на этом API. Без PUBLIC_API_BASE_URL за прокси получается localhost — боты не качают."""
    base = getattr(settings, 'PUBLIC_API_BASE_URL', '') or ''
    path = path if path.startswith('/') else f'/{path}'
    if base:
        return f'{base.rstrip("/")}{path}'
    # После USE_X_FORWARDED_HOST / SECURE_PROXY_SSL_HEADER в settings — совпадает с публичным URL
    return request.build_absolute_uri(path)


def _share_page_public_url(request, chat_id):
    """
    Канонический URL страницы /share/ на API — как в запросе (включая ?v=, ?msg=).
    Совпадает со ссылкой из клиента — важно для Telegram og:url.
    """
    fp = request.get_full_path()
    if not fp.startswith('/'):
        fp = '/' + fp
    return _share_og_absolute_api_url(request, fp)


def _share_og_image_url(request, site_base):
    """
    1) /images/og_share.png или misaimg.png на API — только если файл достаточно большой
       (иначе это может быть синяя заглушка, её не показываем).
    2) WEB_APP_PUBLIC_URL/misa.png — тот же арт, что client/public/misa.png (Миса, не квадрат).
    """
    img_dir = os.path.join(settings.BASE_DIR, 'images')
    base = (site_base or '').strip().rstrip('/')
    for name in ('og_share.png', 'misaimg.png'):
        p = os.path.join(img_dir, name)
        if os.path.isfile(p) and os.path.getsize(p) >= _OG_LOCAL_IMAGE_MIN_BYTES:
            return _share_og_absolute_api_url(request, f'/images/{name}')
    if base:
        return f'{base}/misa.png'
    return ''


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
    HTML с Open Graph для /share/<chat_id>/.
    Краулеры (Telegram и др.) не выполняют JS — читают og:* из <head>.
    og:url и canonical — на публичный URL API (как ссылка шаринга), не на WEB_APP_PUBLIC_URL:
    иначе Telegram запрашивает SPA и теряет превью.
    Браузеры выполняют location.replace() на WEB_APP_PUBLIC_URL (SPA).
    Редирект 302 по User-Agent не используем: у Telegram бывает нестандартный UA.
    """
    public = getattr(settings, 'WEB_APP_PUBLIC_URL', '').strip().rstrip('/')

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

    og_url = _share_page_public_url(request, chat_id)

    og_image = _share_og_image_url(request, site_base)
    og_image_esc = html_escape(og_image) if og_image else ''
    og_w, og_h = _og_share_image_dimensions(og_image)
    twitter_card = 'summary_large_image' if og_image else 'summary'

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
        if og_image.lower().startswith('https://'):
            parts.append(f'<meta property="og:image:secure_url" content="{og_image_esc}" />')
        parts.append(f'<meta property="og:image:alt" content="{og_title}" />')
        if og_w and og_h:
            parts.append(f'<meta property="og:image:width" content="{og_w}" />')
            parts.append(f'<meta property="og:image:height" content="{og_h}" />')
    parts.extend([
        f'<meta name="twitter:card" content="{twitter_card}" />',
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
    ])
    if public and _share_should_redirect_to_spa(request):
        spa_url = public + request.get_full_path()
        parts.append(f'<script>location.replace({json.dumps(spa_url)});</script>')
    parts.extend(['</body>', '</html>'])
    resp = HttpResponse('\n'.join(parts), content_type='text/html; charset=utf-8')
    resp['Cache-Control'] = 'public, max-age=300'
    return resp


def robots_txt(request):
    """Чтобы краулеры (в т.ч. проверка robots перед превью) не получали 401 от JWT middleware."""
    return HttpResponse("User-agent: *\nAllow: /\n", content_type="text/plain; charset=utf-8")


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
