import hashlib
import hmac
import logging
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from typing import Any, Optional

import requests
from requests.adapters import HTTPAdapter

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
_completion_executor = ThreadPoolExecutor(
    max_workers=4,
    thread_name_prefix='gradius-completion',
)
_http_session = requests.Session()
_http_adapter = HTTPAdapter(
    pool_connections=20,
    pool_maxsize=20,
    max_retries=0,
    pool_block=False,
)
_http_session.mount('https://', _http_adapter)
_http_session.mount('http://', _http_adapter)


class GradiusService:
    """Нативная реклама Gradius для диалоговых ответов модели."""

    _pending_enrichments = {}
    _pending_lock = threading.Lock()

    @classmethod
    def max_ads_per_chat(cls) -> int:
        try:
            return max(0, int(os.getenv('GRADIUS_MAX_ADS_PER_CHAT', '10')))
        except (TypeError, ValueError):
            return 10

    @classmethod
    def requests_per_answer(cls) -> int:
        try:
            return max(1, int(os.getenv('GRADIUS_REQUESTS_PER_ANSWER', '1')))
        except (TypeError, ValueError):
            return 1

    @classmethod
    def request_timeout(cls) -> float:
        try:
            value = float(os.getenv('GRADIUS_REQUEST_TIMEOUT_SECONDS', '8'))
            return value if value > 0 else 8.0
        except (TypeError, ValueError):
            return 8.0

    @classmethod
    def ads_before_return(cls) -> int:
        try:
            return max(1, int(os.getenv('GRADIUS_ADS_BEFORE_RETURN', '1')))
        except (TypeError, ValueError):
            return 1

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
        existing_ad_count: int = 0,
    ) -> str:
        """Запрашивает вставки и вставляет native-text-ad по insert_index."""
        if not text or not str(text).strip():
            return text
        if cls._looks_like_media_only(text):
            return text
        remaining = max(0, cls.max_ads_per_chat() - max(0, existing_ad_count))
        if remaining == 0:
            return text

        request_count = min(cls.requests_per_answer(), remaining)

        def request_placement(_request_index):
            return cls._request(
                chat_id=chat_id,
                user_id=user_id,
                role='assistant',
                text=text,
                lang=lang,
                platform=platform,
                model_version=model_version or cls._model_version(),
            )

        placements = []
        completed = set()
        target_ads = min(cls.ads_before_return(), remaining)
        executor = ThreadPoolExecutor(max_workers=request_count)
        futures = [
            executor.submit(request_placement, request_index)
            for request_index in range(request_count)
        ]
        try:
            for future in as_completed(
                futures,
                timeout=cls.request_timeout() + 0.5,
            ):
                completed.add(future)
                placements.extend(future.result())
                ad_count = sum(
                    1 for item in placements
                    if isinstance(item, dict)
                    and item.get('type') == 'native-text-ad'
                )
                if ad_count >= target_ads:
                    # Include responses which completed at the same time, but do
                    # not hold the user response for slow upstream requests.
                    for ready in futures:
                        if ready not in completed and ready.done():
                            completed.add(ready)
                            placements.extend(ready.result())
                    break
        except TimeoutError:
            logging.warning(
                'GradiusService: response collection timed out after %.1fs',
                cls.request_timeout(),
            )

        def collect_all():
            all_placements = []
            try:
                for future in futures:
                    all_placements.extend(future.result())
                return cls.insert_native_ads(
                    str(text),
                    all_placements,
                    max_ads=remaining,
                )
            finally:
                executor.shutdown(wait=True)

        if platform == 'web':
            completion = _completion_executor.submit(collect_all)
            with cls._pending_lock:
                cls._pending_enrichments[str(chat_id)] = completion
        else:
            return collect_all()

        if not placements:
            return text
        return cls.insert_native_ads(str(text), placements, max_ads=remaining)

    @classmethod
    def pop_pending_enrichment(cls, chat_id: str):
        """Return and remove the future containing all late ad responses."""
        with cls._pending_lock:
            return cls._pending_enrichments.pop(str(chat_id), None)

    @classmethod
    def insert_native_ads(
        cls,
        answer: str,
        response: list,
        max_ads: Optional[int] = None,
    ) -> str:
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
        if max_ads is not None:
            ads_sorted = ads_sorted[:max(0, max_ads)]
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
            resp = _http_session.post(
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
                timeout=cls.request_timeout(),
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
