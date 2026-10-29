import html
import re

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
