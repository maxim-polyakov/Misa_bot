import logging
import os
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
        ads = [
            item for item in (response or [])
            if isinstance(item, dict) and item.get('type') == 'native-text-ad'
        ]
        if not ads:
            return answer

        # С конца, чтобы индексы не сдвигались.
        ads_sorted = sorted(
            ads,
            key=lambda item: int(((item.get('content') or {}).get('insert_index') or 0)),
            reverse=True,
        )
        result = answer
        for item in ads_sorted:
            content = item.get('content') or {}
            ad_text = (content.get('content') or '').strip()
            if not ad_text:
                continue
            try:
                insert_index = int(content.get('insert_index') or 0)
            except (TypeError, ValueError):
                insert_index = len(result)
            insert_index = max(0, min(insert_index, len(result)))
            # Как в docs.gradius.pro: вставка по insert_index с пробелами по краям.
            result = f'{result[:insert_index]} {ad_text} {result[insert_index:]}'
        return result

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
