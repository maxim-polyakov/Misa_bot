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
            0: str(ra.answer(0)) + ' ',
            1: 'не за что. ',
            2: 'утверждение про дела. ',
            3: 'утверждение про погоду. ',
            4: 'просьба, оставить неприличные высказывания при себе. '
        }
        return info_dict[chosen_item]

    @classmethod
    def __decision(cls, text_message, emotion, predicts):
        if (text_message.count('?') > 0):
            outlist = []
            answer = cls._qa.answer(text_message)
            outlist.append(answer)
        else:
            outlist = []
            res = cls.__classify(predicts.index(True))
            outlist.append(res)
        outlist.append('' + emotion)
        return outlist

    @classmethod
    def _neurodesc(cls, text, text_message):
#
#
        modelpaths = ['all_set_hi', 'all_set_thanks', 'all_set_business', 'all_set_weather', 'all_set_trash']

        emotion = ''
        predicts = []
        for id in range(0, len(modelpaths)):
            predicts.append(cls._dbc.check(text, modelpaths[id]))

        return cls.__decision(text_message,
                              emotion,
                              predicts)

    @classmethod
    def monitor(cls, message, pltype):
        text = []
        if(pltype == 'discord'):
            lowertext = message.content.lower()
        else:
            lowertext = message.text.lower()
        cls._dbc.insert_to(lowertext)
        outstr = ''
        if (lowertext.count('миса') > 0 or lowertext.lower().count('misa') > 0 or lowertext.count('миса,')):
            lowertext = lowertext.replace('миса ', '').replace('misa ', '').replace('миса,', '').replace('misa,', '')
            text.append(lowertext)
            outlist = cls._neurodesc(text, lowertext)
            if (outlist != None):
                for outmes in outlist:
                    outstr += outmes
            return outstr.capitalize()
        else:
            return outstr.capitalize()
