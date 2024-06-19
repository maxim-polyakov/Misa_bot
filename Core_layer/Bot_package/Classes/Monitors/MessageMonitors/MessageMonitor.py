from pathlib import Path
from Core_layer.Answer_package.Classes import CommonAnswer, QuestionAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor
import os

class MessageMonitor(IMonitor.IMonitor):
    """

    This class is describes object for monitoring messages from chats

    """
    _pr = CommonPreprocessing.CommonPreprocessing()
    _qa = QuestionAnswer.QuestionAnswer()
    _ra = CommonAnswer.RandomAnswer()
    @classmethod
    def __decision(cls, text_message):
#
#
        outlist = []
        if (text_message.count('?') > 0):
            answer = cls._qa.answer(text_message)
        elif(text_message.count('Привет')>0):
            answer = cls._ra.answer((text_message))
        outlist.append(answer)
        outlist.append(' ')
        return outlist

    @classmethod
    def _neurodesc(cls, text, text_message):
#
#
        return cls.__decision(text_message)

    @classmethod
    def monitor(cls, message, pltype):
        text = []
        if(pltype == 'discord'):
            lowertext = message.content.lower()
        else:
            lowertext = message.text.lower()
        idb = DB_Communication.DB_Communication()
        idb.insert_to(lowertext)
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
