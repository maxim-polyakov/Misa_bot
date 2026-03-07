import re
import logging
from Core_layer.Answer_package.Interfaces import IAnswer
from Deep_layer.NLP_package.Classes.GPT import Gpt


class GptAnswer(IAnswer.IAnswer):
    """

    It is class for question answering

    """
    __gpt = Gpt.Gpt()

    @classmethod
    def answer(cls, text, user, is_command_check, chat_id=None):
        # generating answers by gpt
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            generated_text = cls.__gpt.generate(text, user, is_command_check, chat_id=chat_id)
            # log successful completion of the answer generation
            logging.info('The gptanswer.answer process has completed successfully')
            return generated_text
        except Exception as e:
            # log the exception if an error occurs during answer generation
            logging.exception('The exception occurred in questionanswer.answer: ' + str(e))

    @classmethod
    def clear_conversation_history(cls, user=None):
        cls.__gpt.clear_conversation_history(user)

    @classmethod
    def import_history_from_db(cls, user, chat_id, exclude_last=0):
        """Импорт истории чата из БД в контекст GPT. exclude_last: исключить последние N сообщений."""
        Gpt.Gpt.import_history_from_db(user, chat_id, exclude_last)

    @classmethod
    def generate_chat_title_from_message(cls, content):
        """Сгенерировать заголовок по первому сообщению пользователя (сразу при отправке)."""
        if not content or not str(content).strip():
            return None
        try:
            text = str(content)[:500].replace('\n', ' ')
            prompt = (
                "По первому сообщению пользователя сгенерируй краткий заголовок чата (до 28 символов). "
                "Заголовок должен отражать суть или тему. Для приветствий (привет, здравствуй и т.п.) — "
                "'Приветствие и начало общения'. Только заголовок, без кавычек.\n\n"
                f"Сообщение: {text.strip()}"
            )
            result = cls.__gpt.generate(prompt, "title_gen", is_command_check=True, chat_id=None)
            if result and isinstance(result, str):
                title = result.strip()[:28]
                if title and len(title) > 2:
                    return title
        except Exception as e:
            logging.warning(f"generate_chat_title_from_message error: {e}")
        return None

    @classmethod
    def generate_chat_title(cls, messages):
        """Сгенерировать контекстный заголовок чата из сообщений (как у DeepSeek)."""
        if not messages or len(messages) < 2:
            return None
        try:
            context_parts = []
            for m in messages[-6:]:
                role = "user" if str(m.get('user', '')).strip() != 'Misa' else "assistant"
                content = str(m.get('content', ''))[:300].replace('\n', ' ')
                if content.strip():
                    context_parts.append(f"{role}: {content.strip()}")
            if not context_parts:
                return None
            prompt = (
                "На основе диалога ниже сгенерируй краткий заголовок чата (до 28 символов). "
                "Заголовок должен отражать суть разговора. Только заголовок, без кавычек и пояснений.\n\n"
                + "\n".join(context_parts)
            )
            result = cls.__gpt.generate(prompt, "title_gen", is_command_check=True, chat_id=None)
            if result and isinstance(result, str):
                title = result.strip()[:28]
                if title and len(title) > 2:
                    return title
        except Exception as e:
            logging.warning(f"generate_chat_title error: {e}")
        return None
