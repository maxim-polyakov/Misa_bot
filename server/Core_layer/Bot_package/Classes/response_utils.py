import os
import re

_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg')
_COMMAND_MARKERS = ('|command|\n', '|command|')


def clean_command_response(response):
    """Убирает |command| из ответа CommandAnalyzer, возвращает список частей."""
    if not response or not isinstance(response, str):
        return []
    parts = response.replace('|command|\n', '\x00').replace('|command|', '\x00').split('\x00')
    return [p.strip() for p in parts if p.strip()]


def strip_command_markers(text):
    """Убирает служебные |command| из строки (в т.ч. прилипшие к URL)."""
    if not isinstance(text, str):
        return ''
    s = text.strip()
    for marker in _COMMAND_MARKERS:
        if marker in s:
            s = s.split(marker)[0].strip()
    return s


def extract_image_url(text):
    """Возвращает чистый URL изображения или пустую строку."""
    s = strip_command_markers(text)
    if not s:
        return ''
    match = re.search(r'https?://[^\s|<>]+', s)
    return match.group(0) if match else s.split()[0]


def is_image_url(text):
    url = extract_image_url(text)
    if not url.startswith('http'):
        return False
    path = url.lower().split('?')[0]
    return path.endswith(_IMAGE_EXTENSIONS) or '/images/' in path


def is_local_image_path(text):
    if not isinstance(text, str):
        return False
    cleaned_path = text.strip().replace('\n', '')
    if not os.path.exists(cleaned_path) or not os.path.isfile(cleaned_path):
        return False
    return os.path.splitext(cleaned_path)[1].lower() in _IMAGE_EXTENSIONS
