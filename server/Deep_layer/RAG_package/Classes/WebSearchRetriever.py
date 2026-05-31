import logging
import random
import time
from urllib.parse import quote

from duckduckgo_search import DDGS


class WebSearchRetriever:
    """Поиск информации в интернете через DuckDuckGo."""

    _BACKENDS = ('bing', 'html', 'lite', 'auto')
    _REGIONS = ('us-en', 'wt-wt', 'ru-ru')

    @classmethod
    def search(cls, query, max_results=5):
        if not query or not str(query).strip():
            return []

        query = str(query).strip()
        results = cls._search_text(query, max_results)
        if results:
            return results

        results = cls._search_news(query, max_results)
        if results:
            logging.info('WebSearchRetriever: %s news results for "%s"', len(results), query)
            return results

        logging.warning('WebSearchRetriever: no results for "%s"', query)
        return []

    @classmethod
    def _search_text(cls, query, max_results):
        for backend in cls._BACKENDS:
            for region in cls._REGIONS:
                results = cls._fetch_text(query, max_results, backend, region)
                if results:
                    logging.info(
                        'WebSearchRetriever: %s text results for "%s" backend=%s region=%s',
                        len(results), query, backend, region,
                    )
                    return results
        return []

    @classmethod
    def _search_news(cls, query, max_results):
        for region in cls._REGIONS:
            try:
                time.sleep(random.uniform(0.2, 0.5))
                raw = DDGS(timeout=20).news(
                    keywords=query,
                    region=region,
                    safesearch='moderate',
                    max_results=max_results,
                )
                results = cls._normalize_results(raw, query, max_results)
                if results:
                    return results
            except Exception as e:
                logging.warning(
                    'WebSearchRetriever news failed for "%s" region=%s: %s',
                    query, region, e,
                )
        return []

    @classmethod
    def _fetch_text(cls, query, max_results, backend, region):
        try:
            time.sleep(random.uniform(0.2, 0.6))
            raw = DDGS(timeout=20).text(
                keywords=query,
                region=region,
                safesearch='moderate',
                max_results=max_results,
                backend=backend,
            )
            return cls._normalize_results(raw, query, max_results)
        except Exception as e:
            logging.warning(
                'WebSearchRetriever backend=%s region=%s failed for "%s": %s',
                backend, region, query, e,
            )
            return []

    @classmethod
    def _normalize_results(cls, raw, query, max_results):
        results = []
        seen_domains = set()

        for item in raw or []:
            url = (item.get('href') or item.get('link') or item.get('url') or '').strip()
            title = (item.get('title') or '').strip()
            body = (
                item.get('body')
                or item.get('snippet')
                or item.get('description')
                or ''
            ).strip()
            if not url and not body and not title:
                continue
            if not body:
                body = title or url
            if not url:
                url = f'https://duckduckgo.com/?q={quote(query)}'

            domain = url.split('/')[2] if '://' in url else url
            if domain.startswith('www.'):
                domain = domain[4:]
            if domain in seen_domains:
                continue
            seen_domains.add(domain)

            results.append({
                'title': title or domain,
                'url': url,
                'snippet': body[:1000],
            })
            if len(results) >= max_results:
                break

        return results
