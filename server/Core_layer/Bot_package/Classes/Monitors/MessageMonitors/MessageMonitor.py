import logging
import re
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor
from Core_layer.Answer_package.Classes import GptAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.RAG_package.Classes.RagService import RagService


def _text_without_urls_for_misa_trigger(text):
    """
    Убирает из текста фрагменты, похожие на URL, чтобы срабатывание по misa/миса/миша
    не происходило только из-за подстроки в ссылке.
    """
    if not text:
        return text
    s = text
    s = re.sub(r'https?://[^\s<>\]]+', ' ', s, flags=re.IGNORECASE)
    s = re.sub(r'www\.[^\s<>\]]+', ' ', s, flags=re.IGNORECASE)
    s = re.sub(
        r'(^|[\s(>])([^\s<>\]]*misa[^\s<>\]]*\.(?:[a-z0-9-]+\.)+[a-z]{2,}[^\s<>\]]*)',
        r'\1',
        s,
        flags=re.IGNORECASE,
    )
    return s


def _strip_bot_address(text):
    """Убирает обращение к боту (миса, misa, …) из текста."""
    if not text:
        return text
    s = str(text).strip()
    s = re.sub(
        r'^(?:@?\s*)?(?:миса|misa|миша|misha|иса)(?:[,\s:—\-–]+|$)',
        '',
        s,
        count=1,
        flags=re.IGNORECASE,
    )
    s = s.strip()
    s = re.sub(
        r'(?:@?\s*)?(?:миса|misa|миша|misha)(?:[,\s:—\-–]+)?',
        ' ',
        s,
        flags=re.IGNORECASE,
    )
    return re.sub(r'\s+', ' ', s).strip()


def _has_bot_trigger(text, pltype):
    """Discord/Telegram: «миса» — только триггер ответа, не команда."""
    if pltype == 'server':
        return True
    s = _text_without_urls_for_misa_trigger(text or '')
    return (
        s.count('миса') > 0
        or s.lower().count('misa') > 0
        or s.count('миша') > 0
        or s.count('misha') > 0
        or s.count('миса,') > 0
        or s.count('иса') > 0
    )


class MessageMonitor(IMonitor.IMonitor):
    """
    It is class for messaging
    """
    _pr = CommonPreprocessing.CommonPreprocessing()
    _dbc = DB_Communication.DB_Communication()
    _gpta = GptAnswer.GptAnswer()
    __commands = None
    __text_message = None
    __user = None
    __chat_id = None
    __pltype = 'server'

    @classmethod
    def _reply_with_rag(cls, text_message, user, emotion, chat_id=None):
        rag_context = RagService.enrich_query(text_message, user, chat_id=chat_id)
        if not rag_context:
            logging.warning('messagemonitor._reply_with_rag: empty rag_context for: %s', text_message[:80])
        res = cls._gpta.answer(
            text_message, user, False, chat_id=chat_id, rag_context=rag_context
        )
        return [res, emotion]

    @classmethod
    def __decision(cls, text_message, user, emotion, commands, pltype='server', chat_id=None):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            cls.__commands = commands
            cls.__pltype = pltype
            text_message = _strip_bot_address(text_message)
            cls.__text_message = text_message
            cls.__user = user
            cls.__chat_id = chat_id

            # Одинаковая логика для web, Discord и Telegram: check() отделяет команды от всего остального
            if cls.check(text_message, user):
                logging.info('messagemonitor.__decision: command (%s)', pltype)
                return [commands.analyse(text_message, user)]

            logging.info('messagemonitor.__decision: RAG (%s)', pltype)
            return cls._reply_with_rag(text_message, user, emotion, chat_id=chat_id)
        except Exception as e:
            logging.exception('The exception occurred in messagemonitor.__decision: ' + str(e))

    @classmethod
    def _neurodesc(cls, text, user, text_message, command, pltype='server', chat_id=None):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            emotion = ''
            logging.info('The messagemonitor._neurodesc process has completed successfully')
            return cls.__decision(
                text_message, user, emotion, command, pltype=pltype, chat_id=chat_id
            )
        except Exception as e:
            logging.exception('The exception occurred in messagemonitor._neurodesc: ' + str(e))

    @classmethod
    def command_type(cls):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            res = cls.__commands.neurocheck(cls.__text_message, cls.__user)
            return res
        except Exception as e:
            logging.exception('The exception occurred in messagemonitor.command_type: ' + str(e))

    @classmethod
    def check(cls, text_message, user):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            text_message = _strip_bot_address(text_message)
            text_message = text_message.replace('\n', ' ')
            input = (
                "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
                "Сообщение: " + text_message + "\n"
                "Задача: Определи, является ли это командой для бота (приказ выполнить действие), "
                "или это вопрос / обычный диалог.\n\n"
                "ВАЖНО: все вопросы — всегда False. Любое сообщение в вопросительной форме "
                "(знак «?», «какая», «сколько», «что», «где», «когда», «почему», «кто», «как» и т.п.) "
                "помечай как False, даже если тема — погода, цены, новости или факты.\n\n"
                "False (не команда) — любой вопрос, совет, мнение, описание, рассуждение, "
                "просьба объяснить или рассказать.\n"
                "True (команда) — только явный императив выполнить действие без вопросительной формы: "
                "нарисуй, сгенерируй, включи, найди, запусти, отправь и т.п.\n\n"
                "Верни True, если это команда, или False, если нет.\n"
                "Формат ответа: только True или False, без дополнительного текста."
            )
            res = cls._gpta.answer(input, user, True, chat_id=cls.__chat_id)
            return res and res.count("True") > 0
        except Exception as e:
            logging.exception('The exception occurred in messagemonitor.check: ' + str(e))

    @classmethod
    def monitor(cls, message, user, command, pltype, chat_id=None):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if pltype == 'discord':
                lowertext = message.content
            elif pltype == 'telegram':
                lowertext = message.text
            else:
                lowertext = message

            cls._dbc.insert_to(lowertext)

            if not _has_bot_trigger(lowertext, pltype):
                logging.info('messagemonitor.monitor: no bot trigger, skip reply (%s)', pltype)
                return ''

            lowertext = _strip_bot_address(lowertext)
            outlist = cls._neurodesc(
                [lowertext], user, lowertext, command, pltype=pltype, chat_id=chat_id
            )
            if outlist is None:
                return ''
            return ''.join(str(m) for m in outlist)
        except Exception as e:
            logging.exception('The exception occurred in messagemonitor.monitor: ' + str(e))
            return ''

    @classmethod
    def clear_conversation_history(cls, user=None):
        cls._gpta.clear_conversation_history(user)
