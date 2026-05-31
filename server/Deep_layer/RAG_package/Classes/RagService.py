import logging
import re

from Core_layer.Answer_package.Classes import GptAnswer
from Deep_layer.RAG_package.Classes.WebSearchRetriever import WebSearchRetriever


class RagService:
    """RAG: решить, нужен ли поиск, найти информацию в интернете, отдать контекст GPT."""

    _gpta = GptAnswer.GptAnswer()

    _SKIP_PATTERNS = re.compile(
        r'^(привет|здравствуй|hello|hi|hey|спасибо|thanks|ок|ok|да|нет|yes|no)[\s!.?,]*$',
        re.IGNORECASE,
    )

    @classmethod
    def enrich_query(cls, text, user, chat_id=None):
        """Возвращает текст из результатов поиска или None."""
        if not text or not str(text).strip():
            logging.info('RAG: skip — empty text')
            return None

        text = str(text).strip()
        if len(text) < 8 or cls._SKIP_PATTERNS.match(text):
            logging.info('RAG: skip — too short or greeting: %s', text[:80])
            return None

        if not cls._needs_web_search(text, user, chat_id):
            logging.info('RAG: search not needed for: %s', text[:100])
            return None

        search_query = cls._extract_search_query(text, user, chat_id=chat_id)
        results = WebSearchRetriever.search(search_query)

        if not results:
            logging.warning('RAG: empty search results for query="%s"', search_query)
            return None

        logging.info('RAG: retrieved %s sources for query="%s"', len(results), search_query)
        return cls._build_context(results)

    @classmethod
    def _needs_web_search(cls, text, user, chat_id=None):
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
            "Задача: Сформулируй краткий поисковый запрос (3–10 слов) для поиска "
            "информации в интернете по этому сообщению. "
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
    def _build_context(cls, results):
        parts = []
        for i, r in enumerate(results, 1):
            parts.append(
                f"[{i}] {r['title']}\n"
                f"URL: {r['url']}\n"
                f"{r['snippet']}"
            )
        return '\n\n'.join(parts)
