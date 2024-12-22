import logging
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor
from Core_layer.Answer_package.Classes import GptAnswer, RandomAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing


class MessageMonitor(IMonitor.IMonitor):
    """
    It is class for messaging
    """
    _pr = CommonPreprocessing.CommonPreprocessing()
    _dbc = DB_Communication.DB_Communication()
    _gpta = GptAnswer.GptAnswer()

    @classmethod
    def __decision(cls, text_message, emotion, commands):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outlist = []

            if (cls._dbc.checkcommands(text_message)):
                outlist.append(commands.analyse(text_message))
                return outlist
            res = cls._gpta.answer(text_message)
            outlist.append(res)
            outlist.append('' + emotion)
            logging.info('The messagemonitor.__decision is done')
            return outlist
        except Exception as e:
            logging.exception(str('The exception in messagemonitor.__decision ' + str(e)))
    @classmethod
    def _neurodesc(cls, text, text_message, command):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            emotion = ''
            logging.info('The messagemonitor._neurodesc is done')
            return cls.__decision(text_message,
                                emotion,
                                command)
        except Exception as e:
            logging.exception(str('The exception in messagemonitor._neurodesc ' + str(e)))
    @classmethod
    def check(cls, text_message):
        if (cls._dbc.checkcommands(text_message)):
            return True
        else:
            return False
    @classmethod
    def monitor(cls, message, command, pltype):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            text = []
            if(pltype == 'discord'):
                lowertext = message.content.lower()
            elif (pltype=='telegram'):
                lowertext = message.text.lower()
            else:
                lowertext = message.lower()

            cls._dbc.insert_to(lowertext)
            outstr = ''
            if (lowertext.count('миса') > 0
                or lowertext.lower().count('misa')
                or lowertext.count('миша') > 0
                or lowertext.count('misha') > 0
                or lowertext.count('миса,')>0
                or lowertext.count('иса')>0):

                lowertext = (lowertext.replace('миса ', '')
                            .replace('misa ', '')
                            .replace('миса,', '')
                            .replace('misa,', '')
                            .replace('миша', '')
                            .replace('misha', '')
                            .replace('иса', ''))

                text.append(lowertext)
                outlist = cls._neurodesc(text, lowertext, command)
                if (outlist != None):
                    for outmes in outlist:
                        outstr += str(outmes)
                logging.info('The messagemonitor.monitor is done')
                return outstr.capitalize()
            else:
                logging.info('The messagemonitor.monitor is done')
                return outstr.capitalize()
        except Exception as e:
            logging.exception(str('The exception in messagemonitor.monitor ' + str(e)))
