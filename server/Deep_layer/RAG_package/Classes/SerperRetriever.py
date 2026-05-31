import logging
import os

import requests

_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
if os.path.exists(_env_path):
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path, override=True)
    except ImportError:
        pass

_USER_AGENT = 'MisaBot-RAG/1.0'
_SERPER_URL = 'https://google.serper.dev/search'


class SerperRetriever:
    """Google Search через Serper API (https://serper.dev)."""

    @classmethod
    def is_available(cls):
        return bool(cls._api_key())

    @classmethod
    def _api_key(cls):
        return (os.getenv('SERPER_API_KEY') or os.getenv('SERP_API_KEY') or '').strip()

    @classmethod
    def search(cls, query, max_results=8):
        key = cls._api_key()
        if not key or not query or not str(query).strip():
            return []

        query = str(query).strip()
        try:
            resp = requests.post(
                _SERPER_URL,
                headers={
                    'X-API-KEY': key,
                    'Content-Type': 'application/json',
                },
                json={
                    'q': query,
                    'num': min(max_results, 10),
                    'gl': 'us',
                    'hl': 'en',
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logging.warning('SerperRetriever failed for "%s": %s', query[:80], e)
            return []

        results = []
        for item in (data.get('organic') or [])[:max_results]:
            url = (item.get('link') or '').strip()
            title = (item.get('title') or '').strip()
            snippet = (item.get('snippet') or '').strip()
            if not url and not snippet:
                continue
            results.append({
                'title': title or url,
                'url': url or f'https://www.google.com/search?q={query}',
                'snippet': snippet[:1000],
                'source': 'serper',
            })

        logging.info('SerperRetriever: %s results for "%s"', len(results), query[:80])
        return results
