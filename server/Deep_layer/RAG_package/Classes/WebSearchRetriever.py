import logging
import time
import random
from duckduckgo_search import DDGS


class WebSearchRetriever:
    """Retrieve web search results with snippets for RAG context."""

    @classmethod
    def search(cls, query, max_results=5):
        if not query or not str(query).strip():
            return []

        query = str(query).strip()
        results = []

        try:
            time.sleep(random.uniform(0.3, 0.8))
            ddgs = DDGS()
            raw = ddgs.text(keywords=query, region='ru-ru', max_results=max_results)
            seen_domains = set()

            for item in raw or []:
                url = (item.get('href') or '').strip()
                title = (item.get('title') or '').strip()
                body = (item.get('body') or '').strip()
                if not url or not body:
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
            logging.warning(f'WebSearchRetriever.search failed for "{query}": {e}')

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
