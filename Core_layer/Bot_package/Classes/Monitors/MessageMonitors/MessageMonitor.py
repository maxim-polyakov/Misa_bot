from Core_layer.Answer_package.Classes import QuestionAnswer, RandomAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor


class MessageMonitor(IMonitor.IMonitor):

    _pr = CommonPreprocessing.CommonPreprocessing()
    _dbc = DB_Communication.DB_Communication()
    _qa = QuestionAnswer.QuestionAnswer()

    @classmethod
    def __classify(cls, chosen_item):
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
        return info_dict[chosen_item]

    @classmethod
    def __decision(cls, text_message, emotion, commands, predicts):
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
        return outlist

    @classmethod
    def _neurodesc(cls, text, text_message, command):
#
#
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

        return cls.__decision(text_message,
                              emotion,
                              command,
                              predicts)

    @classmethod
    def monitor(cls, message, command, pltype):
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
            return outstr.capitalize()
        else:
            return outstr.capitalize()
