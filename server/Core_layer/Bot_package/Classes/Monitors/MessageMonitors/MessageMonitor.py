import logging
import re
from concurrent.futures import ThreadPoolExecutor
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor
from Core_layer.Answer_package.Classes import GptAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.RAG_package.Classes.RagService import RagService
from Deep_layer.API_package.Classes.GradiusService import GradiusService

_analytics_executor = ThreadPoolExecutor(
    max_workers=2,
    thread_name_prefix='misa-analytics',
)


def _log_background_failure(future):
    try:
        future.result()
    except Exception as error:
        logging.warning('messagemonitor: background analytics failed: %s', error)


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


_SUPPORTED_COMMAND = re.compile(
    r'(?:^|[.!?]\s*)'
    r'(?:абонируй(?:ся)?|нарисуй|нарисовать|изобрази|draw|'
    r'атакуй|атаковать|фас|пиздани|'
    r'найди\s+(?:в\s+)?(?:интернете|google|гугле|википедии)|'
    r'поищи\s+(?:в\s+)?(?:интернете|google|гугле|википедии)|'
    r'предскажи\s+погоду|скажи\s+погоду)\b',
    re.IGNORECASE | re.UNICODE,
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
            # Only a small fixed set of commands has executable handlers.
            # Everything else eventually falls back to the normal GPT answer,
            # so an extra model classification adds latency without changing it.
            return bool(_SUPPORTED_COMMAND.search(text_message))
        except Exception as e:
            logging.exception('The exception occurred in messagemonitor.check: ' + str(e))
            return False

    @classmethod
    def _gradius_ids(cls, message, user, pltype, chat_id=None):
        source_user_id = str(user or '').strip() or 'anonymous'
        if pltype == 'telegram':
            from_user = getattr(message, 'from_user', None)
            if from_user is not None and getattr(from_user, 'id', None) is not None:
                source_user_id = str(from_user.id)
        platform = 'web' if pltype == 'server' else pltype
        gradius_chat_id = (
            str(chat_id).strip()
            if chat_id
            else f'{platform}_{source_user_id}'
        )
        gradius_user_id = GradiusService.pseudonymous_user_id(
            user_id=source_user_id,
            chat_id=gradius_chat_id,
            platform=platform,
        )
        return gradius_chat_id, gradius_user_id, platform

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

            analytics = _analytics_executor.submit(cls._dbc.insert_to, lowertext)
            analytics.add_done_callback(_log_background_failure)

            if not _has_bot_trigger(lowertext, pltype):
                logging.info('messagemonitor.monitor: no bot trigger, skip reply (%s)', pltype)
                return ''

            gradius_chat_id, gradius_user_id, platform = cls._gradius_ids(
                message, user, pltype, chat_id=chat_id
            )
            existing_ad_count = 0
            if pltype == 'server' and chat_id:
                from Core_layer.Chat_package.Classes.ChatService import ChatService
                existing_ad_count = ChatService.count_native_ads(chat_id)

            ad_prefetch = None
            with ThreadPoolExecutor(max_workers=1) as executor:
                tracking = executor.submit(
                    GradiusService.track_user_message,
                    chat_id=gradius_chat_id,
                    user_id=gradius_user_id,
                    text=str(lowertext or ''),
                    platform=platform,
                )
                prefetch_task = None
                if pltype == 'server':
                    prefetch_task = executor.submit(
                        GradiusService.prefetch_assistant_placements,
                        chat_id=gradius_chat_id,
                        user_id=gradius_user_id,
                        targeting_text=str(lowertext or ''),
                        platform=platform,
                        existing_ad_count=existing_ad_count,
                    )

                lowertext = _strip_bot_address(lowertext)
                outlist = cls._neurodesc(
                    [lowertext], user, lowertext, command, pltype=pltype, chat_id=chat_id
                )
                try:
                    tracking.result()
                except Exception as e:
                    logging.warning('messagemonitor.monitor: gradius user track failed: %s', e)
                if prefetch_task is not None:
                    try:
                        ad_prefetch = prefetch_task.result()
                    except Exception as e:
                        logging.warning(
                            'messagemonitor.monitor: gradius prefetch failed: %s',
                            e,
                        )

            if outlist is None:
                return ''
            answer = ''.join(str(m) for m in outlist)
            try:
                answer = GradiusService.enrich_assistant_answer(
                    chat_id=gradius_chat_id,
                    user_id=gradius_user_id,
                    text=answer,
                    platform=platform,
                    existing_ad_count=existing_ad_count,
                    prefetch=ad_prefetch,
                )
            except Exception as e:
                logging.warning('messagemonitor.monitor: gradius assistant enrich failed: %s', e)
            return answer
        except Exception as e:
            logging.exception('The exception occurred in messagemonitor.monitor: ' + str(e))
            return ''

    @classmethod
    def clear_conversation_history(cls, user=None):
        cls._gpta.clear_conversation_history(user)
