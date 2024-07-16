from pathlib import Path
from Deep_layer.NLP_package.Predictors import BinaryLSTM, MultyLSTM
from Core_layer.Answer_package.Answers.Classes import QuestionAnswer, RandomAnswer
from Deep_layer.NLP_package import Mapas
from Deep_layer.NLP_package.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.DB_Bridge import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor
import os

class MessageMonitor(IMonitor.IMonitor):

    _bpred = BinaryLSTM.BinaryLSTM()
    _mpred = MultyLSTM.MultyLSTM()
    _pr = CommonPreprocessing.CommonPreprocessing()
    _dbc = DB_Communication.DB_Communication()
    _mapa = Mapas.Mapa()
    _mapaslist = Mapas.ListMapas()
    _qa = QuestionAnswer.QuestionAnswer()

    @classmethod
    def __classify(cls, chosen_item):
        try:
            ra = RandomAnswer.RandomAnswer()
            info_dict = {
                0: str(ra.answer()) + ' ',
                1: 'не за что. ',
                2: 'утверждение про дела. ',
                3: 'утверждение про погоду. ',
                4: 'просьба, оставить неприличные высказывания при себе. '
            }
            return info_dict[chosen_item]
        except:
            return ''

    @classmethod
    def __decision(cls, text_message, emotion, commands, predicts):
        if (text_message.count('?') > 0):
            outlist = []
            answer = cls._qa.answer(text_message)
            outlist.append(answer)
        else:
            outlist = []
            try:
                outlist.append(cls.__classify(predicts.index(True)))
            except:
                outlist.append(':)')
        outlist.append(' ' + emotion)
        return outlist

    @classmethod
    def _neurodesc(cls, text, text_message, command):
#
#
        modelpaths = ['all_set_hi', 'all_set_thanks', 'all_set_business', 'all_set_weather', 'all_set_trash']
        tokenizerpaths = []

        emotion = ''
        predicts = []
        mapaslist = cls._mapaslist.getlistmapas()
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
        else:
            lowertext = message.text.lower()
        cls._dbc.insert_to(lowertext)
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
