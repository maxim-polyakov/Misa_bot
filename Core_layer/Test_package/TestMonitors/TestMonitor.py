import os
from pathlib import Path
from Core_layer.Test_package.TestMonitors import ITestMonitor
from Deep_layer.NLP_package import Predictors
from Deep_layer.NLP_package import Mapas
from Deep_layer.NLP_package import TextPreprocessers
from Deep_layer.DB_package.DB_Bridge import DB_Communication


class TestMonitor(ITestMonitor.ITestMonitor):

    _bpred = Predictors.BinaryLSTM()
    _mpred = Predictors.MultyLSTM()
    _pr = TextPreprocessers.CommonPreprocessing()
    _dbc = DB_Communication.DB_Communication()
    _mapa = Mapas.Mapa()
    _mapaslist = Mapas.ListMapas()


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
            outlist.append(', ' + emotion)
        else:
            outlist = []
            for predict in predicts:
                outlist.append(cls.__classify(predict))
        outlist.append(', ' + '😊')
        return outlist

    @classmethod
    def _emotionsrecognition(cls, text):
        modelpath = next(Path().rglob('0_emotionsmodel.h5'))
        tokenizerpath = next(Path().rglob('0_emotionstokenizer.pickle'))
        emotion = cls._mpred.predict(text, cls._mapa.EMOTIONSMAPA,
                                     modelpath,
                                     tokenizerpath)
        return emotion

    @classmethod
    def _neurodesc(cls, text, text_message, modelpath):
        modelpaths = []
        tokenizerpaths = []
        fullPathModels = str(next(Path().rglob('models')))
        fullPathTokenizers = str(next(Path().rglob('tokenizers')))
        modelarr = os.listdir(fullPathModels + modelpath)
        tokenizerarr = os.listdir(fullPathTokenizers + modelpath)

        for model in modelarr:
            modelpaths.append(str(fullPathModels) + modelpath + str(model))
        for tokenizer in tokenizerarr:
            tokenizerpaths.append(str(fullPathTokenizers) + modelpath + str(tokenizer))
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
    def monitor(cls, input_df, datatable, modelpath):
        try:
            text = input_df['text']
            outstr = ''
            idx = 1
            for txt in text:
                lowertext = txt.lower()
                outlist = cls._neurodesc(text, lowertext, modelpath)
                if (outlist != None):
                    for outmes in outlist:
                        outstr += outmes
                DB_Communication.DB_Communication.insert_to(idx, lowertext, outstr, datatable)
                idx = idx + 1
        except:
            print('input_df[\'text\'] == None')