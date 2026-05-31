import logging
import random
import re
import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
)

_FACT_PATTERN = re.compile(
    r'(?:\$|€|₽|£|\bUSD\b|\bEUR\b|\bRUB\b|\d+[.,]\d{1,4}|\d+\s*%)',
    re.IGNORECASE,
)

_STOPWORDS = frozenset({
    'как', 'что', 'где', 'когда', 'какой', 'какая', 'какие', 'сколько', 'сейчас',
    'the', 'and', 'for', 'how', 'what', 'when', 'where', 'who', 'why', 'is', 'are',
})


class WebSearchRetriever:
    """
    Универсальный поиск через DuckDuckGo.

    Сниппеты DDG редко содержат цифры (цены, курсы) — поэтому:
    1) собираем больше ссылок с разных backend/region;
    2) загружаем текст с найденных страниц;
    3) ранжируем результаты с конкретными фактами выше.
    """

    _BACKENDS = ('bing', 'html', 'lite', 'auto')
    _REGIONS = ('us-en', 'wt-wt', 'ru-ru')

    @classmethod
    def search_queries(cls, queries, topic='', max_results=5):
        """Поиск по нескольким формулировкам запроса."""
        merged = []
        seen_urls = set()

        for query in queries or []:
            q = str(query).strip()
            if not q:
                continue
            batch = cls._collect_web_results(q, per_query=max_results + 3)
            for item in batch:
                url = item.get('url', '')
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                merged.append(item)

        if not merged:
            logging.warning('WebSearchRetriever: no links for queries=%s', queries)
            return []

        merged = cls._enrich_results(merged, max_pages=5)
        merged = cls._rank_results(merged, topic or ' '.join(queries))
        with_facts = [r for r in merged if not cls._results_lack_facts([r])]
        without_facts = [r for r in merged if cls._results_lack_facts([r])]
        merged = with_facts + without_facts

        logging.info(
            'WebSearchRetriever: %s results after enrich+rank (facts=%s) queries=%s',
            min(len(merged), max_results),
            len(with_facts) > 0,
            [q[:60] for q in queries if q],
        )
        return merged[:max_results]

    @classmethod
    def search(cls, query, max_results=5, symbol_hint_text=None):
        """Один запрос — обёртка над search_queries."""
        topic = (symbol_hint_text or query or '').strip()
        return cls.search_queries([query], topic=topic, max_results=max_results)

    @classmethod
    def results_lack_facts(cls, results):
        return cls._results_lack_facts(results)

    @classmethod
    def _collect_web_results(cls, query, per_query=8):
        merged = []
        seen_domains = set()

        for backend in cls._BACKENDS:
            for region in cls._REGIONS:
                batch = cls._fetch_text(query, per_query, backend, region)
                for item in batch:
                    url = item.get('url', '')
                    domain = cls._domain(url)
                    if domain in seen_domains:
                        continue
                    seen_domains.add(domain)
                    merged.append(item)
                    if len(merged) >= per_query:
                        break
                if len(merged) >= per_query:
                    break
            if len(merged) >= per_query:
                break

        if len(merged) < per_query // 2:
            news = cls._search_news(query, per_query)
            for item in news:
                url = item.get('url', '')
                domain = cls._domain(url)
                if domain in seen_domains:
                    continue
                seen_domains.add(domain)
                merged.append(item)

        logging.info('WebSearchRetriever: collected %s links for "%s"', len(merged), query[:80])
        return merged

    @classmethod
    def _domain(cls, url):
        if '://' not in url:
            return url
        domain = url.split('/')[2]
        return domain[4:] if domain.startswith('www.') else domain

    @classmethod
    def _results_lack_facts(cls, results):
        for r in results or []:
            if _FACT_PATTERN.search(r.get('snippet', '')):
                return False
        return True

    @classmethod
    def _rank_results(cls, results, topic):
        terms = {
            t for t in re.findall(r'[\w\u0400-\u04FF]+', str(topic).lower())
            if len(t) > 2 and t not in _STOPWORDS
        }

        def score(item):
            blob = f"{item.get('title', '')} {item.get('snippet', '')} {item.get('url', '')}".lower()
            s = 0
            if _FACT_PATTERN.search(blob):
                s += 20
            for term in terms:
                if term in blob:
                    s += 3
            if any(x in blob for x in ('how to', 'как узнать', 'лучшие сервисы', 'best apps')):
                s -= 5
            return s

        return sorted(results, key=score, reverse=True)

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
                logging.warning('WebSearchRetriever news failed for "%s": %s', query[:60], e)
        return []

    @classmethod
    def _fetch_text(cls, query, max_results, backend, region):
        try:
            time.sleep(random.uniform(0.15, 0.45))
            raw = DDGS(timeout=20).text(
                keywords=query,
                region=region,
                safesearch='moderate',
                max_results=max_results,
                backend=backend,
            )
            return cls._normalize_results(raw, query, max_results)
        except Exception as e:
            logging.debug(
                'WebSearchRetriever backend=%s region=%s failed for "%s": %s',
                backend, region, query[:60], e,
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

            domain = cls._domain(url)
            if domain in seen_domains or 'duckduckgo.com' in domain:
                continue
            seen_domains.add(domain)

            results.append({
                'title': title or domain,
                'url': url,
                'snippet': body[:800],
            })
            if len(results) >= max_results:
                break

        return results

    @classmethod
    def _enrich_results(cls, results, max_pages=5):
        """Загружает текст страниц — в сниппетах DDG цифр почти нет."""
        if not results:
            return results

        enriched = []
        pages_fetched = 0
        # Сначала загружаем страницы без цифр в сниппете
        ordered = sorted(
            results,
            key=lambda r: 0 if cls._results_lack_facts([r]) else 1,
        )

        for r in ordered:
            item = dict(r)
            url = item.get('url', '')
            if (
                pages_fetched < max_pages
                and url
                and 'duckduckgo.com' not in url
            ):
                page_text = cls._fetch_page_text(url)
                pages_fetched += 1
                if page_text:
                    item['snippet'] = cls._merge_snippet(item.get('snippet', ''), page_text)
            enriched.append(item)

        return enriched

    @classmethod
    def _merge_snippet(cls, snippet, page_text, max_len=4000):
        parts = []
        if snippet and snippet.strip():
            parts.append(snippet.strip())
        if page_text and page_text.strip():
            if not snippet or page_text.strip() not in snippet:
                parts.append(page_text.strip())
        return '\n\n'.join(parts)[:max_len]

    @classmethod
    def _fetch_page_text(cls, url, max_chars=3500):
        try:
            resp = requests.get(
                url,
                headers={'User-Agent': _USER_AGENT, 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8'},
                timeout=12,
                allow_redirects=True,
            )
            resp.raise_for_status()
            content_type = resp.headers.get('Content-Type', '')
            if 'html' not in content_type.lower() and 'text' not in content_type.lower():
                return ''

            soup = BeautifulSoup(resp.text, 'html.parser')
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript', 'svg', 'iframe']):
                tag.decompose()

            og_desc = soup.find('meta', attrs={'property': 'og:description'})
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            meta_text = ''
            if og_desc and og_desc.get('content'):
                meta_text = og_desc['content'].strip()
            elif meta_desc and meta_desc.get('content'):
                meta_text = meta_desc['content'].strip()

            chunks = []
            if meta_text:
                chunks.append(meta_text)
            chunks.extend(soup.stripped_strings)

            text = re.sub(r'\s+', ' ', ' '.join(chunks)).strip()
            return text[:max_chars] if text else ''
        except Exception as e:
            logging.warning('WebSearchRetriever page fetch failed for %s: %s', url, e)
            return ''
