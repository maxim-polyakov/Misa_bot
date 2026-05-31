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

_SYMBOL_HINTS = (
    ('tesla', 'TSLA'),
    ('тесла', 'TSLA'),
    ('apple', 'AAPL'),
    ('эпл', 'AAPL'),
    ('microsoft', 'MSFT'),
    ('майкрософт', 'MSFT'),
    ('google', 'GOOGL'),
    ('alphabet', 'GOOGL'),
    ('amazon', 'AMZN'),
    ('амазон', 'AMZN'),
    ('nvidia', 'NVDA'),
    ('meta', 'META'),
    ('facebook', 'META'),
    ('фейсбук', 'META'),
    ('bitcoin', 'BTC-USD'),
    ('биткоин', 'BTC-USD'),
    ('btc', 'BTC-USD'),
    ('ethereum', 'ETH-USD'),
    ('eth', 'ETH-USD'),
)


class WebSearchRetriever:
    """Поиск в интернете через DuckDuckGo + текст с найденных страниц."""

    _BACKENDS = ('bing', 'html', 'lite', 'auto')
    _REGIONS = ('us-en', 'wt-wt', 'ru-ru')

    @classmethod
    def search(cls, query, max_results=5, symbol_hint_text=None):
        if not query or not str(query).strip():
            return []

        query = str(query).strip()
        hint = (symbol_hint_text or query).strip()
        results = cls._search_text(query, max_results)
        if not results:
            results = cls._search_news(query, max_results)

        if not results:
            logging.warning('WebSearchRetriever: no results for "%s"', query)
            return []

        results = cls._enrich_results(results)
        if cls._results_lack_facts(results):
            quote = cls._fetch_market_quote(hint)
            if quote:
                logging.info('WebSearchRetriever: market quote fallback for "%s"', query)
                results = [quote] + results[: max(0, max_results - 1)]

        logging.info(
            'WebSearchRetriever: %s results for "%s" (facts=%s)',
            len(results), query, not cls._results_lack_facts(results),
        )
        return results

    @classmethod
    def results_lack_facts(cls, results):
        return cls._results_lack_facts(results)

    @classmethod
    def _results_lack_facts(cls, results):
        for r in results or []:
            if _FACT_PATTERN.search(r.get('snippet', '')):
                return False
        return True

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

    @classmethod
    def _enrich_results(cls, results, max_pages=3):
        """Дополняет сниппеты текстом со страниц — в них часто есть цены и цифры."""
        if not results:
            return results

        enriched = []
        pages_fetched = 0

        for r in results:
            item = dict(r)
            snippet = item.get('snippet', '')
            url = item.get('url', '')
            need_page = (
                pages_fetched < max_pages
                and url
                and 'duckduckgo.com' not in url
                and (cls._results_lack_facts([item]) or len(snippet) < 250)
            )
            if need_page:
                page_text = cls._fetch_page_text(url)
                pages_fetched += 1
                if page_text:
                    item['snippet'] = cls._merge_snippet(snippet, page_text)
            enriched.append(item)

        return enriched

    @classmethod
    def _merge_snippet(cls, snippet, page_text, max_len=3500):
        parts = []
        if snippet and snippet.strip():
            parts.append(snippet.strip())
        if page_text and page_text.strip():
            if not snippet or page_text.strip() not in snippet:
                parts.append(page_text.strip())
        merged = '\n\n'.join(parts)
        return merged[:max_len]

    @classmethod
    def _fetch_page_text(cls, url, max_chars=3000):
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

            meta_desc = soup.find('meta', attrs={'name': 'description'})
            meta_text = meta_desc.get('content', '').strip() if meta_desc else ''

            chunks = []
            if meta_text:
                chunks.append(meta_text)
            chunks.extend(soup.stripped_strings)

            text = re.sub(r'\s+', ' ', ' '.join(chunks)).strip()
            if not text:
                return ''
            return text[:max_chars]
        except Exception as e:
            logging.warning('WebSearchRetriever page fetch failed for %s: %s', url, e)
            return ''

    @classmethod
    def _symbol_from_text(cls, text):
        t_lower = str(text).lower()
        for name, symbol in _SYMBOL_HINTS:
            if re.search(rf'\b{re.escape(name)}\b', t_lower):
                return symbol
        m = re.search(r'\b([A-Z]{2,5})\b', str(text))
        if m:
            return m.group(1)
        return None

    @classmethod
    def _fetch_market_quote(cls, text):
        symbol = cls._symbol_from_text(text)
        if not symbol:
            return None
        url = (
            f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
            f'?interval=1d&range=1d'
        )
        try:
            resp = requests.get(
                url,
                headers={'User-Agent': _USER_AGENT},
                timeout=10,
            )
            resp.raise_for_status()
            result = (resp.json().get('chart') or {}).get('result') or []
            if not result:
                return None
            meta = result[0].get('meta') or {}
            price = meta.get('regularMarketPrice') or meta.get('previousClose')
            if price is None:
                return None
            currency = meta.get('currency', 'USD')
            exchange = meta.get('exchangeName') or meta.get('fullExchangeName') or ''
            name = meta.get('longName') or meta.get('shortName') or symbol
            page_url = f'https://finance.yahoo.com/quote/{symbol}'
            snippet = (
                f'{name} ({symbol}): {price} {currency}. '
                f'Биржа: {exchange}. '
                f'Источник: Yahoo Finance, данные на момент запроса.'
            )
            return {
                'title': f'{name} — {price} {currency}',
                'url': page_url,
                'snippet': snippet,
            }
        except Exception as e:
            logging.warning('WebSearchRetriever market quote failed for %s: %s', symbol, e)
            return None
