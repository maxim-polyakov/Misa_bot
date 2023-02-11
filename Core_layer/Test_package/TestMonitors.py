from pathlib import Path
from Deep_layer.NLP_package import Predictors
from Core_layer.Answer_package import Answers
from Deep_layer.NLP_package import Mapas
from Deep_layer.NLP_package import TextPreprocessers
from abc import ABC, abstractmethod
from Deep_layer.DB_package import DB_Bridge
import os


class ITestMonitor(ABC):

    @abstractmethod
    def monitor(self):
        pass

class TestMonitor(ITestMonitor):
    _bpred = Predictors.BinaryLSTM()
    _nnpred = Predictors.NaiveBayes()
    _rfpred = Predictors.RandomForest()
    _mpred = Predictors.MultyLSTM()
    _xgpred = Predictors.Xgboost()
    _pr = TextPreprocessers.CommonPreprocessing()
    _dbc = DB_Bridge.DB_Communication()
    _mapa = Mapas.Mapa()
    _mapaslist = Mapas.ListMapas()
    qa = Answers.QuestionAnswer()

    @classmethod
    def __classify_question(cls, chosen_item):
        try:
            info_dict = {
                'Приветствие': 'Приветствие',
                'Благодарность': 'Благодарность',
                'Дело': 'Дело',
                'Погода': 'Погода',
                'Треш': 'Треш'
            }
            return info_dict[chosen_item]
        except:
            return ''

    @classmethod
    def __classify(cls, chosen_item):
        try:
            info_dict = {
                'Приветствие': 'Приветствие',
                'Благодарность': 'Благодарность',
                'Дело': 'Дело',
                'Погода': 'Погода',
                'Треш': 'Треш'
            }
            return info_dict[chosen_item]
        except:
            return ''

    @classmethod
    def __decision(cls, text_message, emotion, predicts):
        if (cls._dbc.checkcommands(text_message)):
            outlist = []
            outlist.append('Команда')
        elif (text_message.count('?') > 0):
            outlist = []
            for predict in predicts:
                outlist.append(cls.__classify_question(predict))
            outlist.append(' ' + emotion)
        else:
            outlist = []
            for predict in predicts:
                outlist.append(cls.__classify(predict))
        outlist.append(', ' + emotion)
        return outlist

    @classmethod
    def _emotionsrecognition(cls, text):
        modelpath = next(Path().rglob('emotionsmodel.h5'))
        tokenizerpath = next(Path().rglob('emotionstokenizer.pickle'))
        emotion = cls._mpred.predict(text, cls._mapa.EMOTIONSMAPA,
                                     modelpath,
                                     tokenizerpath)
        return emotion

    @classmethod
    def _neurodesc(cls, text, text_message):
        modelpaths = []
        tokenizerpaths = []
        fullPathModels = str(next(Path().rglob('models')))
        fullPathTokenizers = str(next(Path().rglob('tokenizers')))
        modelarr = os.listdir(fullPathModels + '/binary/LSTM/')
        tokenizerarr = os.listdir(fullPathTokenizers + '/binary/LSTM/')

        for model in modelarr:
            modelpaths.append(str(fullPathModels) + '/binary/LSTM/' + str(model))
        for tokenizer in tokenizerarr:
            tokenizerpaths.append(str(fullPathTokenizers) + '/binary/LSTM/' + str(tokenizer))
        emotion = ''
        predicts = []
        mapaslist = cls._mapaslist.getlistmapas()
        for id in range(0, len(modelpaths)):
            predicts.append(cls._bpred.predict(text, mapaslist[id],
                                               modelpaths[id],
                                               tokenizerpaths[id], ''))
        return cls.__decision(text_message,
                              emotion,
                              predicts)

    @classmethod
    def monitor(cls, input_df, datatable):
        text = input_df['text']
        outstr = ''
        idx = 0
        for txt in text:
            lowertext = txt.lower()
            outlist = cls._neurodesc(text, lowertext)
            if (outlist != None):
                for outmes in outlist:
                    outstr += outmes
            DB_Bridge.DB_Communication.insert_to(idx, lowertext, outstr, datatable)

class TestMonitorLSTM(TestMonitor):
    def __init__(self):
        pass
    @classmethod
    def monitor(cls):
        DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets.markedvalidsetlstm')
        df = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text from validation_sets.markedvalidsethuman ORDER BY id ASC')
        datatable = 'markedvalidsetlstm'
        super().monitor(df, datatable)

class TestMonitorNaiveBayes(TestMonitor):
    def __init__(self):
        pass
    @classmethod
    def monitor(cls):
        DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets.markedvalidsetnaivebayes')

        df = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text from validation_sets.markedvalidsethuman ORDER BY id ASC')
        datatable = 'markedvalidsetnaivebayes'
        super().monitor(df, datatable)


class TestMonitorRandomForest(TestMonitor):
    def __init__(self):
        pass
    @classmethod
    def monitor(cls):
        DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets.markedvalidsetrandomforest')

        df = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text from validation_sets.markedvalidsethuman ORDER BY id ASC')
        datatable = 'markedvalidsetrandomforest'
        super().monitor(df, datatable)
