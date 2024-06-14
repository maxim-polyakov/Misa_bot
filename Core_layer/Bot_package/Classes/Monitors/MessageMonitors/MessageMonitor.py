from pathlib import Path
from Deep_layer.NLP_package.Classes.Predictors import MultyLSTM
from Deep_layer.NLP_package.Classes.Predictors import BinaryLSTM
from Core_layer.Answer_package.Classes import RandomAnswer, QuestionAnswer
from Deep_layer.NLP_package import Mapas
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor
import os

class MessageMonitor(IMonitor.IMonitor):
    """

    This class is describes object for monitoring messages from chats

    """
    _bpred = BinaryLSTM.BinaryLSTM()
    _mpred = MultyLSTM.MultyLSTM()
    _pr = CommonPreprocessing.CommonPreprocessing()
    _dbc = DB_Communication.DB_Communication()
    _mapa = Mapas.Map()
    _mapaslist = Mapas.ListMapas()
    _qa = QuestionAnswer.QuestionAnswer()

    @classmethod
    def __classify(cls, chosen_item):
        try:
            ra = RandomAnswer.RandomAnswer()
            info_dict = {
                'Приветствие': str(ra.answer()[0]) + ' ',
                'Благодарность': 'не за что. ',
                'Дело': 'утверждение про дела. ',
                'Погода': 'утверждение про погоду. ',
                'Треш': 'просьба, оставить неприличные высказывания при себе. '
            }
            return info_dict[chosen_item]
        except:
            return ''

    @classmethod
    def __decision(cls, text_message, commands):
        outlist = []
        if (cls._dbc.checkcommands(cls._pr.preprocess_text(text_message))):
            return commands.analyse(text_message)
        elif (text_message.count('?') > 0):
            answer = cls._qa.answer(text_message)
            outlist.append(answer)
        outlist.append(' ')
        return outlist

    @classmethod
    def _emotionsrecognition(cls, text):
        modelpath = next(Path().rglob('0_lstmemotionsmodel.h5'))
        tokenizerpath = next(Path().rglob('0_lstmemotionstokenizer.pickle'))
        emotion = cls._mpred.predict(text, cls._mapa.EMOTIONSMAPA,
                                     modelpath,
                                     tokenizerpath)
        return emotion

    @classmethod
    def _neurodesc(cls, text, text_message, command):
#
#
        return cls.__decision(text_message,
                              command)

    @classmethod
    def monitor(cls, message, command, pltype):
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
            outlist = cls._neurodesc(text, lowertext, command)
            if (outlist != None):
                for outmes in outlist:
                    outstr += outmes
            return outstr.capitalize()
        else:
            return outstr.capitalize()
