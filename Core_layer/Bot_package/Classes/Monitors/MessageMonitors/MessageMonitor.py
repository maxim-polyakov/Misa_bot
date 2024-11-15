import logging
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor
from Core_layer.Answer_package.Classes import QuestionAnswer, RandomAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing


class MessageMonitor(IMonitor.IMonitor):
    """
    It is class for messaging
    """
    _pr = CommonPreprocessing.CommonPreprocessing()
    _dbc = DB_Communication.DB_Communication()
    _qa = QuestionAnswer.QuestionAnswer()

    @classmethod
    def __classify(cls, chosen_item):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            ra = RandomAnswer.RandomAnswer()
            info_dict = {
                0: str(ra.answer('hianswer')) + ' ',
                1: str(ra.answer('thanksanswer')) + ' ',
                2: str(ra.answer('businessanswer')) + ' ',
                3: str(ra.answer('weatheranswer')) + ' ',
                4: str(ra.answer('trashanswer')) + ' ',
                5: str(ra.answer('moodanswer')) + ' ',
                6: str(ra.answer('helathanswer')) + ' '
            }
            logging.info('The messagemonitor.__classify is done')
            return info_dict[chosen_item]
        except Exception as e:
            logging.exception(str('The exception in messagemonitor.__classify ' + str(e)))
    @classmethod
    def __decision(cls, text_message, emotion, commands, predicts):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outlist = []

            if (cls._dbc.checkcommands(text_message)):
                outlist.append(commands.analyse(text_message))
                return outlist
            if True in predicts:
                res = cls.__classify(predicts.index(True))
            else:
                res = 'Нет классификации. '
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
            modelpaths = ['all_set_hi',
                        'all_set_thanks',
                        'all_set_business',
                        'all_set_weather',
                        'all_set_trash',
                        'all_set_mood',
                        'all_set_health']

            emotion = ''
            predicts = []
            for id in range(0, len(modelpaths)):
                predicts.append(cls._dbc.check(text, modelpaths[id]))


            logging.info('The messagemonitor._neurodesc is done')
            return cls.__decision(text_message,
                                emotion,
                                command,
                                predicts)
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
                        outstr += outmes
                logging.info('The messagemonitor.monitor is done')
                return outstr.capitalize()
            else:
                logging.info('The messagemonitor.monitor is done')
                return outstr.capitalize()
        except Exception as e:
            logging.exception(str('The exception in messagemonitor.monitor ' + str(e)))
