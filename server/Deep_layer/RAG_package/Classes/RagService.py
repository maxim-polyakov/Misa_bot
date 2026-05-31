import logging
import re

from Core_layer.Answer_package.Classes import GptAnswer
from Deep_layer.RAG_package.Classes.WebSearchRetriever import WebSearchRetriever


class RagService:
    """RAG pipeline: decide if web search is needed, retrieve context, inject into GPT."""

    _gpta = GptAnswer.GptAnswer()

    _SKIP_PATTERNS = re.compile(
        r'^(привет|здравствуй|hello|hi|hey|спасибо|thanks|ок|ok|да|нет|yes|no)[\s!.?,]*$',
        re.IGNORECASE,
    )

    # Явные запросы актуальных данных — без дополнительного GPT-решения
    _NEEDS_SEARCH_HEURISTIC = re.compile(
        r'(?:'
        r'сейчас|сегодня|на\s+(?:данный\s+)?момент|актуальн|текущ(?:ая|ий|ее|ие)?|'
        r'курс|цена|стоит|стоимость|котировк|'
        r'bitcoin|биткоин|btc|ethereum|eth|криптовалют|'
        r'акци(?:й|и|я|ю)|stock|nasdaq|'
        r'новост(?:и|ей|ь)|'
        r'сколько\s+стоит|какой\s+курс|какая\s+цена'
        r')',
        re.IGNORECASE | re.UNICODE,
    )

    _WIKI_HEURISTIC = re.compile(
        r'(?:кто\s+такой|что\s+такое|биографи|истори(?:я|и)|определени|википеди)',
        re.IGNORECASE | re.UNICODE,
    )

    _FINANCIAL_HEURISTIC = re.compile(
        r'(?:'
        r'цена|стоимость|котировк|курс|'
        r'акци(?:й|и|я|ю|ей)|stock|nasdaq|nyse|'
        r'bitcoin|биткоин|btc|ethereum|eth|криптовалют|crypto'
        r')',
        re.IGNORECASE | re.UNICODE,
    )

    _TICKER_HINTS = (
        ('tesla', 'TSLA'),
        ('тесла', 'TSLA'),
        ('apple', 'AAPL'),
        ('эпл', 'AAPL'),
        ('апple', 'AAPL'),
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
    )

    @classmethod
    def enrich_query(cls, text, user, chat_id=None):
        """Run RAG pipeline. Returns context string for GPT or None if search not needed."""
        if not text or not str(text).strip():
            return None

        text = str(text).strip()
        if len(text) < 8 or cls._SKIP_PATTERNS.match(text):
            return None

        if not cls._needs_web_search(text, user, chat_id):
            logging.info(f'RAG: search not needed for: {text[:100]}')
            return None

        search_query = cls._extract_search_query(text, user, chat_id=chat_id)
        is_financial = cls._is_financial_query(text)
        use_wiki = False if is_financial else cls._prefer_wikipedia(text, user, chat_id=chat_id)

        if use_wiki:
            results = WebSearchRetriever.search_wikipedia(search_query)
            if not results:
                results = WebSearchRetriever.search(search_query)
        else:
            results = WebSearchRetriever.search(search_query)
            if not results and not is_financial:
                results = WebSearchRetriever.search_wikipedia(search_query)

        if not results:
            logging.warning(f'RAG: empty search results for query="{search_query}"')
            return None

        logging.info(f'RAG: retrieved {len(results)} sources for query="{search_query}"')
        return cls._build_context(results)

    @classmethod
    def _needs_web_search_heuristic(cls, text):
        return bool(cls._NEEDS_SEARCH_HEURISTIC.search(text))

    @classmethod
    def _needs_web_search(cls, text, user, chat_id=None):
        if cls._needs_web_search_heuristic(text):
            logging.info(f'RAG: heuristic web search trigger: {text[:100]}')
            return True

        prompt = (
            "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
            f"Сообщение: {text}\n\n"
            "Задача: Нужен ли поиск актуальной информации в интернете для ответа на это сообщение?\n"
            "True — если вопрос про текущие события, новости, погоду, курсы валют, цены, "
            "актуальные данные, факты которые могли измениться, или пользователь явно просит найти/узнать что-то.\n"
            "False — если это общий разговор, творческая задача, код, советы, мнения, "
            "исторические факты, математика, перевод, или ответ можно дать без интернета.\n\n"
            "Формат ответа: только True или False."
        )
        try:
            result = cls._gpta.answer(prompt, user, True, chat_id=chat_id)
            if isinstance(result, dict):
                return False
            needs = result and 'True' in str(result)
            logging.info(f'RAG: GPT search decision={needs} for: {text[:100]}')
            return needs
        except Exception as e:
            logging.warning(f'RAG needs_web_search check failed: {e}')
            return cls._needs_web_search_heuristic(text)

    @classmethod
    def _is_financial_query(cls, text):
        return bool(cls._FINANCIAL_HEURISTIC.search(text))

    @classmethod
    def _build_financial_search_query(cls, text):
        t_lower = str(text).lower()
        for name, ticker in cls._TICKER_HINTS:
            if name in t_lower:
                return f'{ticker} stock price today'
        if re.search(r'btc|bitcoin|биткоин', t_lower):
            return 'bitcoin price today USD'
        if re.search(r'eth|ethereum', t_lower):
            return 'ethereum price today USD'
        return f'{str(text).strip()[:80]} stock price today'

    @classmethod
    def _extract_search_query(cls, text, user, chat_id=None):
        if cls._is_financial_query(text):
            return cls._build_financial_search_query(text)
        if cls._needs_web_search_heuristic(text):
            return text[:200]

        prompt = (
            "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
            f"Сообщение: {text}\n\n"
            "Задача: Сформулируй краткий поисковый запрос (3-8 слов) для поиска актуальной информации "
            "в интернете. Верни только запрос, без пояснений и кавычек."
        )
        try:
            result = cls._gpta.answer(prompt, user, True, chat_id=chat_id)
            if isinstance(result, dict) or not result:
                return text[:120]
            query = str(result).strip().strip('"\'')
            return query[:200] if query else text[:120]
        except Exception as e:
            logging.warning(f'RAG extract_search_query failed: {e}')
            return text[:120]

    @classmethod
    def _prefer_wikipedia(cls, text, user, chat_id=None):
        if cls._is_financial_query(text):
            return False
        if cls._needs_web_search_heuristic(text):
            return bool(cls._WIKI_HEURISTIC.search(text))

        prompt = (
            "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
            f"Сообщение: {text}\n\n"
            "Задача: Лучше искать в Википедии (True) или в общем интернете (False)?\n"
            "True — биографии, история, наука, определения, энциклопедические темы.\n"
            "False — новости, погода, цены, актуальные события, инструкции, отзывы.\n\n"
            "Формат ответа: только True или False."
        )
        try:
            result = cls._gpta.answer(prompt, user, True, chat_id=chat_id)
            if isinstance(result, dict):
                return False
            return result and 'True' in str(result)
        except Exception:
            return False

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
