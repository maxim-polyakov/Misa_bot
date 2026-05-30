import logging
import time
import random
from duckduckgo_search import DDGS


class WebSearchRetriever:
    """Retrieve web search results with snippets for RAG context."""

    _BACKENDS = ('auto', 'html', 'lite')

    @classmethod
    def search(cls, query, max_results=5):
        if not query or not str(query).strip():
            return []

        query = str(query).strip()

        for backend in cls._BACKENDS:
            results = cls._search_with_backend(query, max_results, backend)
            if results:
                logging.info(f'WebSearchRetriever: {len(results)} results via backend={backend}')
                return results

        logging.warning(f'WebSearchRetriever: no results for "{query}"')
        return []

    @classmethod
    def _search_with_backend(cls, query, max_results, backend):
        results = []
        try:
            time.sleep(random.uniform(0.2, 0.6))
            raw = DDGS().text(
                keywords=query,
                region='wt-wt',
                safesearch='moderate',
                max_results=max_results,
                backend=backend,
            )
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
                    continue

                domain = url.split('/')[2] if '://' in url else url
                if domain.startswith('www.'):
                    domain = domain[4:]
                if domain in seen_domains:
                    continue
                seen_domains.add(domain)

                results.append({
                    'title': title or domain,
                    'url': url,
                    'snippet': body[:600],
                })
                if len(results) >= max_results:
                    break

        except Exception as e:
            logging.warning(f'WebSearchRetriever backend={backend} failed for "{query}": {e}')

        return results

    @classmethod
    def search_wikipedia(cls, query):
        try:
            import wikipedia as w
            w.set_lang('ru')
            summary = w.summary(query, sentences=4, auto_suggest=True, redirect=True)
            if summary:
                return [{
                    'title': f'Wikipedia: {query}',
                    'url': f'https://ru.wikipedia.org/wiki/{query.replace(" ", "_")}',
                    'snippet': summary[:800],
                }]
        except Exception as e:
            logging.debug(f'Wikipedia search failed for "{query}": {e}')
        return []
