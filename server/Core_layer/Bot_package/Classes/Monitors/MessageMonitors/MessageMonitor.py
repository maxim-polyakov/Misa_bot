import logging
import re
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor
from Core_layer.Answer_package.Classes import GptAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing


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
    # без схемы, но в имени хоста есть misa: misa.example.ru/share
    s = re.sub(
        r'(^|[\s(>])([^\s<>\]]*misa[^\s<>\]]*\.(?:[a-z0-9-]+\.)+[a-z]{2,}[^\s<>\]]*)',
        r'\1',
        s,
        flags=re.IGNORECASE,
    )
    return s


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

    @classmethod
    def __decision(cls, text_message, user, emotion, commands, chat_id=None):
        # call gpt to get an answer and check commands
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outlist = []
            cls.__commands = commands
            cls.__text_message = text_message
            cls.__user = user
            cls.__chat_id = chat_id
            if (cls.check(text_message, user)):
                # analyze the command and add the result to the output list
                outlist.append(commands.analyse(text_message, user))
                return outlist
            res = cls._gpta.answer(text_message, user, False, chat_id=chat_id)
            outlist.append(res)
            # append the emotion to the output list
            outlist.append('' + emotion)
            # log successful completion of the process
            logging.info('The messagemonitor.__decision process has completed successfully')
            return outlist
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in messagemonitor.__decision: ' + str(e))

    @classmethod
    def _neurodesc(cls, text, user, text_message, command, chat_id=None):
        # calling the decision with emotion
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # initialize an empty emotion variable
            emotion = ''
            # log successful execution of the method
            logging.info('The messagemonitor._neurodesc process has completed successfully')
            # call the __decision method with the provided parameters
            return cls.__decision(text_message, user, emotion, command, chat_id=chat_id)
        except Exception as e:
            # log the exception if an error occurs
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
            text_message = text_message.replace('\n', ' ')
            input = (
                    "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
                    "Сообщение: " + text_message + "\n"
                    "Задача: Определи, является ли это командой, строго учитывая контекст высказывания. "
                    "Считается командой: (1) прямое побуждение к действию (приказ, просьба, инструкция); "
                    "(2) любое сообщение о погоде — вопрос про погоду, запрос погоды, рассказ о погоде и т.п. "
                    "Не считается командой: советы, рекомендации, описания, размышления, эмоции или повествование "
                    "(кроме погодной тематики), даже при глаголах в повелительном наклонении. "
                    "Верни True, если это команда, или False, если нет.\n"
                    "Формат ответа: только True или False, без дополнительного текста."
            )
            res = cls._gpta.answer(input, user, True, chat_id=cls.__chat_id)

            if res.count("True") > 0:
                logging.info('The messagemonitor.check process has completed successfully')
                return True
            else:
                logging.info('The messagemonitor.check process has completed successfully')
                return False
        except Exception as e:
            logging.exception('The exception occurred in messagemonitor.check: ' + str(e))

    @classmethod
    def monitor(cls, message, user, command, pltype, chat_id=None):
        # main monitor for calculating messages
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            text = []
            # determine the message content based on the platform type
            if(pltype == 'discord'):
                lowertext = message.content
            elif (pltype=='telegram'):
                lowertext = message.text
            else:
                lowertext = message
            # insert the processed text into the database
            cls._dbc.insert_to(lowertext)
            outstr = ''
            text_for_trigger = _text_without_urls_for_misa_trigger(lowertext)
            # check if the message contains specific keywords (не в части ссылки)
            if (text_for_trigger.count('миса') > 0
                or text_for_trigger.lower().count('misa') > 0
                or text_for_trigger.count('миша') > 0
                or text_for_trigger.count('misha') > 0
                or text_for_trigger.count('миса,') > 0
                or text_for_trigger.count('иса') > 0 and pltype != 'server'):
                # perform text replacements (currently empty replacements)
                lowertext = (lowertext.replace('миса ', '')
                             .replace('misa ', '')
                             .replace('миса,', '')
                             .replace('misa,', '')
                             .replace('миша', '')
                             .replace('misha', '')
                             .replace('иса', '')
                             .replace('Миса', '')
                             .replace('Misa ', '')
                             .replace('Миса,', '')
                             .replace('Misa,', '')
                             .replace('Миша', '')
                             .replace('Misha', '')
                             .replace('Иса', ''))
                text.append(lowertext)
                outlist = cls._neurodesc(text, user, lowertext, command, chat_id=chat_id)
                # if the function returns a result, format it into a string
                if (outlist != None):
                    for outmes in outlist:
                        outstr += str(outmes)
                # log successful completion of the process
                logging.info('The messagemonitor.monitor process has completed successfully')
                return outstr
            else:
                if pltype == 'server':
                    # perform text replacements (currently empty replacements)
                    lowertext = (lowertext.replace('миса ', '')
                                 .replace('misa ', '')
                                 .replace('миса,', '')
                                 .replace('misa,', '')
                                 .replace('миша', '')
                                 .replace('misha', '')
                                 .replace('иса', '')
                                 .replace('Миса', '')
                                 .replace('Misa ', '')
                                 .replace('Миса,', '')
                                 .replace('Misa,', '')
                                 .replace('Миша', '')
                                 .replace('Misha', '')
                                 .replace('Иса', ''))
                    text.append(lowertext)
                    outlist = cls._neurodesc(text, user, lowertext, command, chat_id=chat_id)
                    # if the function returns a result, format it into a string
                    if (outlist != None):
                        for outmes in outlist:
                            outstr += str(outmes)
                    # log successful completion of the process
                    logging.info('The messagemonitor.monitor process has completed successfully')
                    return outstr
                # log successful completion even if no keywords were found
                logging.info('The messagemonitor.monitor process has completed successfully')
                return outstr
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in messagemonitor.monitor: ' + str(e))

    @classmethod
    def clear_conversation_history(cls, user=None):
        cls._gpta.clear_conversation_history(user)
