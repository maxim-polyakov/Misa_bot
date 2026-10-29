import html
import re

from Deep_layer.API_package.Classes.GradiusService import GradiusService

_MD_LINK_RE = re.compile(r'\[([^\]]+)\]\((https?://[^)\s]+)\)')


def markdown_links_to_telegram_html(text: str) -> str:
    """Экранирует HTML и превращает markdown-ссылки в <a href>."""
    if not text:
        return ''
    parts = []
    last = 0
    for match in _MD_LINK_RE.finditer(text):
        parts.append(html.escape(text[last:match.start()]))
        label = html.escape(match.group(1))
        url = html.escape(match.group(2), quote=True)
        parts.append(f'<a href="{url}">{label}</a>')
        last = match.end()
    parts.append(html.escape(text[last:]))
    return ''.join(parts)


def has_markdown_link(text: str) -> bool:
    return bool(text and _MD_LINK_RE.search(text))


def format_telegram_reply(text: str) -> tuple[str, str | None]:
    """
    Готовит текст для Telegram.
    Возвращает (html_or_plain, parse_mode) — parse_mode 'HTML' или None.
    Реклама всегда снизу, с подписью и кликабельной ссылкой.
    """
    body, ads = GradiusService.split_ads(text or '')
    if not ads and not has_markdown_link(body):
        return text or '', None

    parts = []
    if body.strip():
        parts.append(markdown_links_to_telegram_html(body.strip()))

    for ad in ads:
        ad_html = markdown_links_to_telegram_html(ad)
        parts.append(f'────────\n<i>Реклама</i>\n{ad_html}')

    if not parts:
        return text or '', None
    return '\n\n'.join(parts), 'HTML'
