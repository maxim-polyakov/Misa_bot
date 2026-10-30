import hashlib
import hmac
import logging
import os
import re
from typing import Any, Optional

import requests

_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
if os.path.exists(_env_path):
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path, override=True)
    except ImportError:
        pass

_DEFAULT_BASE_URL = 'https://api.adlean.pro'
_ENDPOINT = '/v1/native/dialogue_model/chat'
AD_START = '<<<misa-ad>>>'
AD_END = '<<</misa-ad>>>'


class GradiusService:
    """Нативная реклама Gradius для диалоговых ответов модели."""

    @classmethod
    def is_enabled(cls) -> bool:
        flag = (os.getenv('GRADIUS_ENABLED') or 'true').strip().lower()
        if flag in ('0', 'false', 'no', 'off'):
            return False
        return bool(cls._api_key())

    @classmethod
    def _api_key(cls) -> str:
        return (os.getenv('GRADIUS_API_KEY') or '').strip()

    @classmethod
    def _base_url(cls) -> str:
        return (os.getenv('GRADIUS_BASE_URL') or _DEFAULT_BASE_URL).rstrip('/')

    @classmethod
    def _model_version(cls) -> Optional[str]:
        value = (os.getenv('GRADIUS_MODEL_VERSION') or 'gpt-4o').strip()
        return value or None

    @classmethod
    def pseudonymous_user_id(
        cls,
        *,
        user_id: str,
        chat_id: str,
        platform: str,
    ) -> str:
        """Возвращает стабильный для чата ID, не раскрывающий ID аккаунта."""
        secret = (
            os.getenv('GRADIUS_USER_ID_SECRET')
            or os.getenv('DJANGO_SECRET_KEY')
            or cls._api_key()
            or 'misa-gradius-user-id-v1'
        )
        payload = '\0'.join((
            str(platform or 'web').strip() or 'web',
            str(user_id or 'anonymous').strip() or 'anonymous',
            str(chat_id or '').strip(),
        ))
        digest = hmac.new(
            str(secret).encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()
        return f'misa_{digest[:32]}'

    @classmethod
    def track_user_message(
        cls,
        *,
        chat_id: str,
        user_id: str,
        text: str,
        lang: str = 'ru',
        platform: str = 'web',
    ) -> list:
        """Сохраняет контекст пользователя (обычно без рекламы)."""
        return cls._request(
            chat_id=chat_id,
            user_id=user_id,
            role='user',
            text=text,
            lang=lang,
            platform=platform,
            model_version=None,
        )

    @classmethod
    def enrich_assistant_answer(
        cls,
        *,
        chat_id: str,
        user_id: str,
        text: str,
        lang: str = 'ru',
        platform: str = 'web',
        model_version: Optional[str] = None,
    ) -> str:
        """Запрашивает вставки и вставляет native-text-ad по insert_index."""
        if not text or not str(text).strip():
            return text
        if cls._looks_like_media_only(text):
            return text

        placements = cls._request(
            chat_id=chat_id,
            user_id=user_id,
            role='assistant',
            text=text,
            lang=lang,
            platform=platform,
            model_version=model_version or cls._model_version(),
        )
        if not placements:
            return text
        return cls.insert_native_ads(str(text), placements)

    @classmethod
    def insert_native_ads(cls, answer: str, response: list) -> str:
        """Всегда добавляет рекламу в конец ответа в маркерах <<<misa-ad>>>…<<</misa-ad>>>."""
        ads = [
            item for item in (response or [])
            if isinstance(item, dict) and item.get('type') == 'native-text-ad'
        ]
        if not ads:
            return answer

        # Порядок по insert_index (как вернул Gradius), но блок целиком — снизу.
        ads_sorted = sorted(
            ads,
            key=lambda item: int(((item.get('content') or {}).get('insert_index') or 0)),
        )
        blocks = []
        for item in ads_sorted:
            content = item.get('content') or {}
            ad_text = (content.get('content') or '').strip()
            if ad_text:
                blocks.append(f'{AD_START}\n{ad_text}\n{AD_END}')
        if not blocks:
            return answer

        base = str(answer or '').rstrip()
        joined = '\n'.join(blocks)
        return f'{base}\n\n{joined}' if base else joined

    @classmethod
    def split_ads(cls, text: str) -> tuple[str, list[str]]:
        """Отделяет тело ответа от блоков <<<misa-ad>>>."""
        if not text or AD_START not in text:
            return str(text or ''), []
        pattern = re.compile(
            re.escape(AD_START) + r'\s*([\s\S]*?)\s*' + re.escape(AD_END),
            re.IGNORECASE,
        )
        ads = [m.group(1).strip() for m in pattern.finditer(text) if m.group(1).strip()]
        body = pattern.sub('', text).rstrip()
        return body, ads

    @classmethod
    def _looks_like_media_only(cls, text: str) -> bool:
        s = str(text).strip()
        if not s:
            return True
        if s.startswith('/images/'):
            return True
        if s.startswith('http://') or s.startswith('https://'):
            lower = s.lower().split('?', 1)[0]
            return lower.endswith((
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.mp4', '.webm'
            ))
        return False

    @classmethod
    def _request(
        cls,
        *,
        chat_id: str,
        user_id: str,
        role: str,
        text: str,
        lang: str,
        platform: str,
        model_version: Optional[str],
    ) -> list:
        if not cls.is_enabled():
            return []
        key = cls._api_key()
        chat_id = str(chat_id or '').strip()
        user_id = str(user_id or '').strip()
        text = str(text or '').strip()
        if not key or not chat_id or not user_id or not text:
            return []

        params: dict[str, Any] = {
            'chat_id': chat_id,
            'user_id': user_id,
            'role': role,
            'lang': (lang or 'ru').strip() or 'ru',
        }
        if model_version:
            params['model_version'] = model_version

        url = f'{cls._base_url()}{_ENDPOINT}'
        try:
            resp = requests.post(
                url,
                params=params,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Auth': key,
                },
                json={
                    'text': text,
                    'user_metadata': {
                        'platform': platform or 'web',
                    },
                },
                timeout=12,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logging.warning('GradiusService.%s failed: %s', role, e)
            return []

        if not isinstance(data, list):
            logging.warning('GradiusService: unexpected response type %s', type(data).__name__)
            return []
        return data
