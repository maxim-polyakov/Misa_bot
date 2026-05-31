import logging
import re
import time

from Core_layer.Answer_package.Classes import GptAnswer
from Deep_layer.RAG_package.Classes.WebSearchRetriever import WebSearchRetriever


class RagService:
    """RAG: решить, нужен ли поиск, найти информацию в интернете, отдать контекст GPT."""

    _gpta = GptAnswer.GptAnswer()
    _cache = {}
    _CACHE_TTL = 90

    _SKIP_PATTERNS = re.compile(
        r'^(привет|здравствуй|hello|hi|hey|спасибо|thanks|ок|ok|да|нет|yes|no)[\s!.?,]*$',
        re.IGNORECASE,
    )

    # Актуальные данные — всегда ищем, без GPT-решения (стабильнее)
    _REALTIME_HEURISTIC = re.compile(
        r'(?:'
        r'сейчас|сегодня|актуальн|текущ|'
        r'цена|стоимость|котировк|курс|'
        r'акци(?:й|и|я|ю|ей)|stock|'
        r'погод|новост|'
        r'bitcoin|биткоин|btc|ethereum|eth|криптовалют'
        r')',
        re.IGNORECASE | re.UNICODE,
    )

    @classmethod
    def enrich_query(cls, text, user, chat_id=None):
        """Возвращает текст из результатов поиска или None."""
        if not text or not str(text).strip():
            logging.info('RAG: skip — empty text')
            return None

        text = str(text).strip()
        cache_key = text.lower()
        cached = cls._cache.get(cache_key)
        if cached and time.time() - cached[0] < cls._CACHE_TTL:
            logging.info('RAG: cache hit for: %s', text[:80])
            return cached[1]

        if len(text) < 8 or cls._SKIP_PATTERNS.match(text):
            logging.info('RAG: skip — too short or greeting: %s', text[:80])
            return None

        if not cls._needs_web_search(text, user, chat_id):
            logging.info('RAG: search not needed for: %s', text[:100])
            return None

        queries = cls._build_search_queries(text, user, chat_id=chat_id)
        logging.info('RAG: search queries=%s', [q[:80] for q in queries])

        results = cls._search_with_fallbacks(text, user, queries, chat_id=chat_id)

        if not results:
            logging.warning('RAG: empty search results for queries=%s', queries)
            return None

        with_facts = [r for r in results if not WebSearchRetriever.results_lack_facts([r])]
        without_facts = [r for r in results if WebSearchRetriever.results_lack_facts([r])]
        results = (with_facts + without_facts)[:5]

        if not with_facts:
            logging.warning('RAG: no numeric facts in results for: %s', text[:80])

        context = cls._build_context(results)
        if with_facts:
            cls._cache[cache_key] = (time.time(), context)

        logging.info(
            'RAG: retrieved %s sources (%s with facts)',
            len(results), len(with_facts),
        )
        return context

    @classmethod
    def _search_with_fallbacks(cls, text, user, queries, chat_id=None):
        """Ищем по списку запросов; если нет цифр — добавляем детерминированные варианты."""
        seen_urls = set()
        results = []

        def merge(batch):
            for item in batch or []:
                url = item.get('url', '')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    results.append(item)

        merge(WebSearchRetriever.search_queries(queries, topic=text, max_results=8))

        if not WebSearchRetriever.results_lack_facts(results):
            return results[:5]

        for q in cls._deterministic_queries(text):
            if q not in queries:
                logging.info('RAG: deterministic retry query="%s"', q[:80])
                merge(WebSearchRetriever.search_queries([q], topic=text, max_results=5))
                if not WebSearchRetriever.results_lack_facts(results):
                    break

        if WebSearchRetriever.results_lack_facts(results):
            refined = cls._refine_search_query(text, user, chat_id=chat_id)
            if refined and refined not in queries:
                logging.info('RAG: refine search query="%s"', refined[:80])
                merge(WebSearchRetriever.search_queries([refined], topic=text, max_results=5))

        with_facts = [r for r in results if not WebSearchRetriever.results_lack_facts([r])]
        without_facts = [r for r in results if WebSearchRetriever.results_lack_facts([r])]
        return (with_facts + without_facts)[:5]

    @classmethod
    def _deterministic_queries(cls, text):
        """Стабильные запросы без GPT — для цен, курсов, акций."""
        queries = []
        t_lower = text.lower()
        latin_words = re.findall(r'[A-Za-z]{2,}', text)

        for word in latin_words:
            w = word.strip()
            if len(w) < 2:
                continue
            queries.append(f'{w} stock price today')
            queries.append(f'{w} stock price USD')

        if cls._REALTIME_HEURISTIC.search(text):
            queries.append(text[:200])

        # уникальные, порядок сохраняем
        seen = set()
        out = []
        for q in queries:
            q = q.strip()
            if q and q not in seen:
                seen.add(q)
                out.append(q)
        return out

    @classmethod
    def _build_search_queries(cls, text, user, chat_id=None):
        queries = []
        # Актуальные данные: сначала стабильные запросы, GPT — дополнение
        if cls._REALTIME_HEURISTIC.search(text):
            queries.extend(cls._deterministic_queries(text))
        else:
            primary = cls._extract_search_query(text, user, chat_id=chat_id)
            if primary:
                queries.append(primary)
            queries.append(text[:200])

        seen = set()
        out = []
        for q in queries:
            q = str(q).strip()
            if q and q not in seen:
                seen.add(q)
                out.append(q)
        return out

    @classmethod
    def _needs_web_search(cls, text, user, chat_id=None):
        if cls._REALTIME_HEURISTIC.search(text):
            logging.info('RAG: heuristic search=True for: %s', text[:100])
            return True

        prompt = (
            "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
            f"Сообщение: {text}\n\n"
            "Задача: Нужен ли поиск информации в интернете для ответа на это сообщение?\n"
            "True — если для ответа нужны актуальные или конкретные факты из интернета: "
            "новости, погода, цены, курсы, события, статистика, определения, "
            "или пользователь просит найти / узнать / проверить что-то.\n"
            "False — если это общий разговор, творческая задача, код, советы, мнения, "
            "математика, перевод, или ответ можно дать без поиска.\n\n"
            "Формат ответа: только True или False."
        )
        try:
            result = cls._gpta.answer(prompt, user, True, chat_id=chat_id)
            if isinstance(result, dict):
                return False
            needs = result and 'True' in str(result)
            logging.info('RAG: search decision=%s for: %s', needs, text[:100])
            return needs
        except Exception as e:
            logging.warning('RAG needs_web_search check failed: %s', e)
            return True

    @classmethod
    def _extract_search_query(cls, text, user, chat_id=None):
        prompt = (
            "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
            f"Сообщение: {text}\n\n"
            "Задача: Сформулируй поисковый запрос (3–12 слов) для Google.\n"
            "Правила:\n"
            "- Запрос должен находить страницы с конкретными фактами и цифрами, "
            "а не статьи «как узнать», «лучшие сервисы», «обзор».\n"
            "- Для международных компаний, акций, курсов, криптовалют — используй English "
            "и тикеры/названия (например Tesla TSLA stock price today).\n"
            "- Для локальных тем — язык пользователя.\n"
            "Верни только запрос, без пояснений и кавычек."
        )
        try:
            result = cls._gpta.answer(prompt, user, True, chat_id=chat_id)
            if isinstance(result, dict) or not result:
                return text[:200]
            query = str(result).strip().strip('"\'')
            return query[:200] if query else text[:200]
        except Exception as e:
            logging.warning('RAG extract_search_query failed: %s', e)
            return text[:200]

    @classmethod
    def _refine_search_query(cls, text, user, chat_id=None):
        prompt = (
            "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
            f"Сообщение пользователя: {text}\n\n"
            "Предыдущий поиск не дал страниц с конкретными цифрами.\n"
            "Сформулируй другой поисковый запрос для Google, который найдёт "
            "страницу с точным значением (цена, курс, температура, дата, число).\n"
            "Используй English для акций/крипты. Верни только запрос."
        )
        try:
            result = cls._gpta.answer(prompt, user, True, chat_id=chat_id)
            if isinstance(result, dict) or not result:
                return None
            query = str(result).strip().strip('"\'')
            return query[:200] if query else None
        except Exception as e:
            logging.warning('RAG refine_search_query failed: %s', e)
            return None

    @classmethod
    def _build_context(cls, results):
        parts = []
        for i, r in enumerate(results, 1):
            parts.append(
                f"[{i}] {r['title']}\n"
                f"URL: {r['url']}\n"
                f"{r['snippet']}"
            )
        return '\n\n'.join(parts)
