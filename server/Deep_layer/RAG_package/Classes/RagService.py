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

    @classmethod
    def enrich_query(cls, text, user, chat_id=None):
        """Run RAG pipeline. Returns context string for GPT or None if search not needed."""
        if not text or not str(text).strip():
            return None

        text = str(text).strip()
        if len(text) < 8 or cls._SKIP_PATTERNS.match(text):
            return None

        if not cls._needs_web_search(text, user, chat_id):
            return None

        search_query = cls._extract_search_query(text, user)

        use_wiki = cls._prefer_wikipedia(text, user)
        if use_wiki:
            results = WebSearchRetriever.search_wikipedia(search_query)
            if not results:
                results = WebSearchRetriever.search(search_query)
        else:
            results = WebSearchRetriever.search(search_query)
            if not results:
                results = WebSearchRetriever.search_wikipedia(search_query)

        if not results:
            return None

        return cls._build_context(results)

    @classmethod
    def _needs_web_search(cls, text, user, chat_id=None):
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
            return result and 'True' in str(result)
        except Exception as e:
            logging.warning(f'RAG needs_web_search check failed: {e}')
            return False

    @classmethod
    def _extract_search_query(cls, text, user):
        prompt = (
            "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
            f"Сообщение: {text}\n\n"
            "Задача: Сформулируй краткий поисковый запрос (3-8 слов) для поиска актуальной информации "
            "в интернете. Верни только запрос, без пояснений и кавычек."
        )
        try:
            result = cls._gpta.answer(prompt, user, True)
            if isinstance(result, dict) or not result:
                return text[:120]
            query = str(result).strip().strip('"\'')
            return query[:200] if query else text[:120]
        except Exception as e:
            logging.warning(f'RAG extract_search_query failed: {e}')
            return text[:120]

    @classmethod
    def _prefer_wikipedia(cls, text, user):
        prompt = (
            "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
            f"Сообщение: {text}\n\n"
            "Задача: Лучше искать в Википедии (True) или в общем интернете (False)?\n"
            "True — биографии, история, наука, определения, энциклопедические темы.\n"
            "False — новости, погода, цены, актуальные события, инструкции, отзывы.\n\n"
            "Формат ответа: только True или False."
        )
        try:
            result = cls._gpta.answer(prompt, user, True)
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
