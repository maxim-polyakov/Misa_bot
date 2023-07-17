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
    def __decision(cls, text_message, emotion, commands, predicts):
        if (cls._dbc.checkcommands(cls._pr.preprocess_text(text_message))):
            return commands.analyse(text_message)
        elif (text_message.count('?') > 0):
            outlist = []
            answer = cls._qa.answer(text_message)
            outlist.append(answer)
        else:
            outlist = []
            for predict in predicts:
                outlist.append(cls.__classify(predict))
        outlist.append(' ' + emotion)
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
        fullPathModels = str(next(Path().rglob('models')))
        fullPathTokenizers = str(next(Path().rglob('tokenizers')))
        modelarr = os.listdir(fullPathModels + '/binary/LSTM/')
        tokenizerarr = os.listdir(fullPathTokenizers + '/binary/LSTM/')
        modelpaths = []
        tokenizerpaths = []
        for model in modelarr:
            modelpaths.append(str(fullPathModels) + '/binary/LSTM/' + str(model))
        for tokenizer in tokenizerarr:
            tokenizerpaths.append(str(fullPathTokenizers) + '/binary/LSTM/' + str(tokenizer))
        emotion = cls._emotionsrecognition(text)
        predicts = []
        mapaslist = cls._mapaslist.getlistmapas()
        for id in range(0, len(modelpaths)):
            predicts.append(cls._bpred.predict(text, mapaslist[id], modelpaths[id], tokenizerpaths[id]))

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
        DB_Communication.DB_Communication.insert_to(lowertext)
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
