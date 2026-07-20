import json
import os
import re
import struct
from html import escape as html_escape
from urllib.parse import quote

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from Core_layer.Controller_package.Classes import Controller
from . import og_preview

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
    path_only = og_image_url.split('?', 1)[0].rstrip('/').lower()
    if path_only.split('/')[-1] == 'misa.png':
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


# Google OAuth
def oauth_google_redirect(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_redirect(request)


def oauth_google_callback(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_callback(request)


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
        if og_image.lower().split('?', 1)[0].endswith('.png'):
            parts.append('<meta property="og:image:type" content="image/png" />')
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
        parts.append(f'<meta name="twitter:image:alt" content="{og_title}" />')
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


def _normalize_ui_locale_code(raw: str):
    code = (raw or "").strip().replace("_", "-")
    if not code:
        return None
    if code in og_preview.TAGLINES:
        return code
    short = code.split("-", 1)[0]
    if short in og_preview.TAGLINES:
        return short
    return None


def spa_og_preview(request):
    """HTML SPA с og:* по Accept-Language (Discord, Telegram и др.)."""
    return og_preview.spa_og_preview_response(request)


def robots_txt(request):
    """Чтобы краулеры (в т.ч. проверка robots перед превью) не получали 401 от JWT middleware."""
    return HttpResponse("User-agent: *\nAllow: /\n", content_type="text/plain; charset=utf-8")


def swagger_ui_html(request):
    """Swagger UI без локальных /static/dmr assets, чтобы nginx static location не ломал страницу."""
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Misa API</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.32.1/swagger-ui.css" />
  <style>
    html, body, #swagger-ui { margin: 0; min-height: 100%; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.32.1/swagger-ui-bundle.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.32.1/swagger-ui-standalone-preset.js"></script>
  <script>
    window.onload = function () {
      window.ui = SwaggerUIBundle({
        url: "/swagger.json",
        dom_id: "#swagger-ui",
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        layout: "StandaloneLayout",
        persistAuthorization: true,
        displayRequestDuration: true
      });
    };
  </script>
</body>
</html>"""
    return HttpResponse(html, content_type="text/html; charset=utf-8")
