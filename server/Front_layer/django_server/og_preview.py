"""
Open Graph для SPA (/chat и др.). Язык превью (как в настройках сайта):
  1) query ?lang= в X-Original-URI (клиент подставляет из getLanguage / localStorage);
  2) cookie misa_locale (если бот передал);
  3) Accept-Language (если пусто — en).

Картинка превью — тот же файл, что client/public/misa.png (в сборке — /misa.png на веб-домене).
В meta: og:image = {WEB_APP_PUBLIC_URL}/misa.png (как %PUBLIC_URL%/misa.png в index.html).
Строки текста — client/src/utils/ogPreviewStrings.js (TAGLINES).
"""
import os
import re
from html import escape as html_escape
from urllib.parse import parse_qs, unquote

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed

_EN = "Misa Chat — modern messenger"
TAGLINES = {
    "en": _EN,
    "ru": "Misa Chat — современный мессенджер",
    "de": "Misa Chat — moderner Messenger",
    "ar": "Misa Chat — مراسل عصري",
    "sq": "Misa Chat — mesazhier modern",
    "am": "Misa Chat — ዘመናዊ መልዕክተኛ",
    "hy": "Misa Chat — ժամանակակից մեսենջեր",
    "az": "Misa Chat — müasir mesencer",
    "eu": "Misa Chat — messenger modernoa",
    "be": "Misa Chat — сучасны месенджар",
    "bn": "Misa Chat — আধুনিক মেসেঞ্জার",
    "bg": "Misa Chat — модерен месинджър",
    "my": "Misa Chat — ခေတ်မီမက်ဆေ့ခ်ျ",
    "ca": "Misa Chat — missatger modern",
    "zh": "Misa Chat — 现代即时通讯",
    "zh-TW": "Misa Chat — 現代即時通訊",
    "hr": "Misa Chat — moderan glasnik",
    "cs": "Misa Chat — moderní messenger",
    "da": "Misa Chat — moderne messenger",
    "nl": "Misa Chat — moderne messenger",
    "et": "Misa Chat — kaasaegne messenger",
    "fi": "Misa Chat — moderni messenger",
    "fr": "Misa Chat — messager moderne",
    "gl": "Misa Chat — mensaxeiro moderno",
    "ka": "Misa Chat — თანამედროვე მესენჯერი",
    "el": "Misa Chat — σύγχρονος αγγελιοφόρος",
    "he": "Misa Chat — שליח מודרני",
    "hi": "Misa Chat — आधुनिक मैसेंजर",
    "hu": "Misa Chat — modern üzenetküldő",
    "is": "Misa Chat — nútímalegur sendill",
    "id": "Misa Chat — messenger modern",
    "ga": "Misa Chat — teachtaire nua-aimseartha",
    "it": "Misa Chat — messenger moderno",
    "ja": "Misa Chat — モダンなメッセンジャー",
    "kn": "Misa Chat — ಆಧುನಿಕ ಮೆಸೆಂಜರ್",
    "kk": "Misa Chat — заманауи мессенджер",
    "km": "Misa Chat — កម្មវិធីសារទំនើប",
    "ko": "Misa Chat — 모던 메신저",
    "lo": "Misa Chat — ຜູ້ສົ່ງຂໍ້ຄວາມທັນສະໄໝ",
    "lv": "Misa Chat — mūsdienīgs ziņotājs",
    "lt": "Misa Chat — šiuolaikiškas messengeris",
    "mk": "Misa Chat — модерен гласник",
    "ms": "Misa Chat — messenger moden",
    "ml": "Misa Chat — ആധുനിക മെസഞ്ചർ",
    "mt": "Misa Chat — messagger modern",
    "mr": "Misa Chat — आधुनिक मेसेंजर",
    "mn": "Misa Chat — орчин үеийн мессенжер",
    "ne": "Misa Chat — आधुनिक मेसेन्जर",
    "nb": "Misa Chat — moderne messenger",
    "fa": "Misa Chat — پیام‌رسان مدرن",
    "pl": "Misa Chat — nowoczesny komunikator",
    "pt": "Misa Chat — mensageiro moderno",
    "pa": "Misa Chat — ਆਧੁਨਿਕ ਮੈਸੇਂਜਰ",
    "ro": "Misa Chat — messenger modern",
    "sr": "Misa Chat — модеран гласник",
    "si": "Misa Chat — නවීන පණිවිඩකරු",
    "sk": "Misa Chat — moderný messenger",
    "sl": "Misa Chat — sodobni messenger",
    "es": "Misa Chat — mensajería moderna",
    "sw": "Misa Chat — mjumbe wa kisasa",
    "tl": "Misa Chat — modernong messenger",
    "tg": "Misa Chat — паёмбари муосир",
    "th": "Misa Chat — แชททันสมัย",
    "tr": "Misa Chat — modern mesajlaşma",
    "uk": "Misa Chat — сучасний месенджер",
    "ur": "Misa Chat — جدید پیغام‌رساں",
    "uz": "Misa Chat — zamonaviy messenger",
    "vi": "Misa Chat — ứng dụng nhắn tin hiện đại",
    "cy": "Misa Chat — negesydd modern",
    "xh": "Misa Chat — umthunywa wexesha",
    "yi": "Misa Chat — מאָדערנער מעסענדזשער",
    "yo": "Misa Chat — oluranṣẹ ọ̀hún",
    "zu": "Misa Chat — isithunywa sesimanje",
    "gu": "Misa Chat — આધુનિક મેસેંજર",
    "haw": "Misa Chat — messenger hou",
    "ig": "Misa Chat — onyeozi ozi",
}

SUPPORTED_CODES = frozenset(TAGLINES.keys())


def _intl_html_lang(code: str) -> str:
    m = {"zh": "zh-CN", "zh-TW": "zh-TW", "pt": "pt-BR", "nb": "nb-NO", "pa": "pa-IN"}
    return m.get(code, code)


def _clean_lang_param(value: str) -> str:
    """
    Убирает хвост после ошибочного второго «?» в значении lang
    (например ?lang=haw?v=1 вместо ?lang=haw&v=1 — иначе lang=«haw?v=1» и не совпадает с TAGLINES).
    """
    s = (value or "").strip()
    if not s:
        return ""
    if "?" in s:
        s = s.split("?", 1)[0].strip()
    if "&" in s:
        s = s.split("&", 1)[0].strip()
    return s


def _lang_from_query_string(qs: str) -> str:
    """lang из query исходного URL (X-Original-URI), т.к. запрос к Django идёт на /og/preview/ без этих параметров."""
    if not qs:
        return ""
    try:
        params = parse_qs(qs, keep_blank_values=False)
        for key in ("lang", "locale", "l"):
            vals = params.get(key)
            if vals and vals[0]:
                return _clean_lang_param(vals[0].strip())
    except (TypeError, ValueError):
        pass
    return ""


def locale_from_request(request, lang_from_uri: str = "") -> str:
    raw = _clean_lang_param(
        (request.GET.get("lang") or "").strip() or (lang_from_uri or "").strip()
    )
    if not raw:
        raw = (request.COOKIES.get("misa_locale") or "").strip()
    if raw:
        low = raw.lower().replace("_", "-")
        if low in TAGLINES:
            return low
        if low.split("-")[0] in TAGLINES:
            return low.split("-")[0]
    al = (request.META.get("HTTP_ACCEPT_LANGUAGE") or "").strip()
    if not al:
        return "en"
    return _parse_accept_language(al)


def _parse_accept_language(header: str) -> str:
    if not header:
        return "en"
    parts = []
    for item in header.split(","):
        item = item.strip()
        if not item:
            continue
        if ";" in item:
            lang, rest = item.split(";", 1)
            q = 1.0
            for piece in rest.split(";"):
                piece = piece.strip()
                if piece.startswith("q="):
                    try:
                        q = float(piece[2:].strip())
                    except ValueError:
                        pass
                    break
        else:
            lang, q = item, 1.0
        lang = lang.strip().lower().replace("_", "-")
        parts.append((lang, q))
    parts.sort(key=lambda x: -x[1])

    for lang, _ in parts:
        if lang in SUPPORTED_CODES:
            return lang
        if lang in ("zh-hk", "zh-tw") or "hant" in lang:
            return "zh-TW"
        if lang.startswith("zh"):
            return "zh"
        short = lang.split("-", 1)[0]
        if short in SUPPORTED_CODES:
            return short
    return "en"


def public_misa_image_url(site_base: str) -> str:
    """Тот же файл, что client/public/misa.png → {WEB_APP_PUBLIC_URL}/misa.png (без query)."""
    base = (site_base or "").strip().rstrip("/")
    return f"{base}/misa.png"


def _safe_spa_path(path_only: str) -> str:
    p = unquote(path_only or "").strip() or "/chat"
    if ".." in p or p.startswith("//"):
        return "/chat"
    if not p.startswith("/"):
        p = "/" + p
    return p[:2048]


def _sub_meta_attr(html: str, pattern: str, content: str) -> str:
    """Подставляет content между группами 1 и 2; без rf\"\\1\" — иначе backslash в тексте ломает замену."""

    def repl(m):
        return m.group(1) + content + m.group(2)

    out, n = re.subn(pattern, repl, html, count=1)
    return out if n else html


def _sub_full(html: str, pattern: str, replacement: str) -> str:
    out, n = re.subn(pattern, replacement, html, count=1)
    return out if n else html


def inject_og_meta(html: str, preview: str, og_page_url: str, site_base: str) -> str:
    esc = html_escape(preview, quote=True)
    url_esc = html_escape(og_page_url, quote=True)
    img_esc = html_escape(public_misa_image_url(site_base), quote=True)

    # Сначала картинка (как в _minimal_html / index.html — до длинного Unicode в title/description):
    # у части краулеров превью ломается, если og:image идёт после «тяжёлых» мета.
    for prop in ("og:image", "og:image:secure_url"):
        html = _sub_meta_attr(
            html,
            rf'(<meta\s+property="{re.escape(prop)}"\s+content=")[^"]*(")',
            img_esc,
        )
    for name in ("twitter:image",):
        html = _sub_meta_attr(
            html,
            rf'(<meta\s+name="{re.escape(name)}"\s+content=")[^"]*(")',
            img_esc,
        )
    html = _sub_meta_attr(
        html,
        r'(<link\s+rel="image_src"\s+href=")[^"]*(")',
        img_esc,
    )

    html = _sub_meta_attr(
        html,
        r'(<meta\s+name="description"\s+content=")[^"]*(")',
        esc,
    )
    for prop in ("og:title", "og:description"):
        html = _sub_meta_attr(
            html,
            rf'(<meta\s+property="{re.escape(prop)}"\s+content=")[^"]*(")',
            esc,
        )
    for name in ("twitter:title", "twitter:description"):
        html = _sub_meta_attr(
            html,
            rf'(<meta\s+name="{re.escape(name)}"\s+content=")[^"]*(")',
            esc,
        )
    html = _sub_meta_attr(
        html,
        r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
        url_esc,
    )
    html = _sub_meta_attr(
        html,
        r'(<link\s+rel="canonical"\s+href=")[^"]*(")',
        url_esc,
    )
    return html


def inject_og_meta_with_locale(html: str, preview: str, og_page_url: str, site_base: str, lang: str) -> str:
    html = inject_og_meta(html, preview, og_page_url, site_base)
    hl = _intl_html_lang(lang)
    html = _sub_full(
        html,
        r'<html\s+lang="[^"]*"',
        f'<html lang="{html_escape(hl, quote=True)}"',
    )
    return html


def _minimal_html(preview: str, og_page_url: str, site_base: str, lang: str) -> str:
    esc = html_escape(preview, quote=True)
    url_esc = html_escape(og_page_url, quote=True)
    img = html_escape(public_misa_image_url(site_base), quote=True)
    hl = _intl_html_lang(lang)
    return f"""<!DOCTYPE html>
<html lang="{hl}">
<head>
<meta charset="utf-8"/>
<meta property="og:image" content="{img}"/>
<meta property="og:image:secure_url" content="{img}"/>
<meta property="og:image:type" content="image/png"/>
<meta property="og:image:width" content="800"/>
<meta property="og:image:height" content="1120"/>
<meta property="og:image:alt" content="Misa AI"/>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5"/>
<meta name="theme-color" content="#000000"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Misa AI"/>
<meta property="og:url" content="{url_esc}"/>
<meta name="description" content="{esc}"/>
<meta property="og:title" content="{esc}"/>
<meta property="og:description" content="{esc}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{esc}"/>
<meta name="twitter:description" content="{esc}"/>
<meta name="twitter:image" content="{img}"/>
<link rel="canonical" href="{url_esc}"/>
<link rel="image_src" href="{img}"/>
<title>Misa AI Chat</title>
</head>
<body>
<noscript><a href="{url_esc}">Misa AI Chat</a></noscript>
<div id="root"></div>
</body>
</html>
"""


def spa_og_preview_response(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    raw = (
        request.META.get("HTTP_X_ORIGINAL_URI", "")
        or request.META.get("HTTP_X_FORWARDED_URI", "")
        or request.GET.get("p")
        or request.GET.get("path")
        or "/chat"
    )
    raw = unquote(str(raw).strip() or "/chat")
    if ".." in raw or raw.startswith("//"):
        raw = "/chat"
    if "?" in raw:
        path_only, qs = raw.split("?", 1)
    else:
        path_only, qs = raw, ""
    path_only = _safe_spa_path(path_only)
    qs = (qs or "").strip()[:2048]

    lang_from_uri = _lang_from_query_string(qs)

    site = getattr(settings, "WEB_APP_PUBLIC_URL", "") or "https://misa.baxic.ru"
    site = site.rstrip("/")
    og_page_url = f"{site}{path_only}?{qs}" if qs else f"{site}{path_only}"

    lang = locale_from_request(request, lang_from_uri=lang_from_uri)
    preview = TAGLINES.get(lang, _EN)

    index_path = getattr(settings, "SPA_INDEX_HTML_PATH", None) or ""
    index_path = str(index_path).strip()
    if index_path and os.path.isfile(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                html = f.read()
        except OSError:
            html = _minimal_html(preview, og_page_url, site, lang)
    else:
        html = _minimal_html(preview, og_page_url, site, lang)

    html = inject_og_meta_with_locale(html, preview, og_page_url, site, lang)
    resp = HttpResponse(html, content_type="text/html; charset=utf-8")
    resp["Cache-Control"] = "public, max-age=300"
    img_abs = public_misa_image_url(site)
    resp["Link"] = f'<{img_abs}>; rel=preload; as=image'
    return resp
