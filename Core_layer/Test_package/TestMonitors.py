from Deep_layer.NLP_package import Predictors
from Deep_layer.NLP_package import Mapas
from Deep_layer.NLP_package import TextPreprocessers
from Deep_layer.DB_package import DB_Bridge
from abc import ABC, abstractmethod
from Core_layer.Bot_package import Botoevaluaters


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

    _be = Botoevaluaters.Binaryevaluate()
    _me = Botoevaluaters.Multyevaluate()
    _mapa = Mapas.Mapa()

    def __init__(self):
        pass

    @classmethod
    def _classify_question(cls, chosen_item):
        info_dict = {
            'Дело': 'Вопрос про дело ',
            'Погода': 'Вопрос про погоду '
        }
        return info_dict.get(chosen_item, 'Вопрос без классификации ')

    @classmethod
    def _classify(cls, chosen_item):
        # ra = Bot_package.Answers.RandomAnswer()
        info_dict = {
            'Приветствие': 'Приветствие ',
            'Благодарность': 'Благодарность ',
            'Дело': 'Дело ',
            'Погода': 'Погода '
        }
        return info_dict.get(chosen_item, 'Нет классификации ')

    @classmethod
    def _emotionsrecognition(cls, text):
        emotion = cls._mpred.predict(text, cls._mapa.EMOTIONSMAPA,
                                     './models/multy/LSTM/emotionsmodel.h5',
                                     './tokenizers/multy/LSTM/emotionstokenizer.pickle')
        return emotion

    @classmethod
    def _decision(cls, text_message, emotion, b_predictor, w_predictor, hi_predictor, th_predictor):
        if (cls._dbc.checkcommands(text_message)):
            outlist = ['Команда ']
            outlist.append(", " + emotion)
            return outlist
        elif (text_message.count('?') > 0):
            outlist = []
            outlist.append(cls._classify_question(w_predictor))
            outlist.append(cls._classify_question(b_predictor))
            outlist = list(set(outlist))
            outlistuncleaned = ['Вопрос без классификации ']
            try:
                outlist.remove('Вопрос без классификации ')
            except:
                return ["exception"]
            outlistcleaned = outlist
            if (len(outlistcleaned) == 0):
                outlistuncleaned.append(", " + emotion)
                return outlistuncleaned
            else:
                outlistcleaned.append(", " + emotion)
                return outlistcleaned
        else:
            outlist = []
            outlist.append(cls._classify(w_predictor))
            outlist.append(cls._classify(b_predictor))
            outlist.append(cls._classify(hi_predictor))
            outlist.append(cls._classify(th_predictor))
            outlist = list(set(outlist))
            outlistuncleaned = ['Нет классификации ']
            try:
                outlist.remove('Нет классификации ')
            except:
                return ['Exception', ", " + emotion]
            outlistcleaned = outlist

            if (len(outlistcleaned) == 0):
                outlistuncleaned.append(", " + emotion)
                return outlistuncleaned
            else:
                outlistcleaned.append(", " + emotion)
                return outlistcleaned

    @classmethod
    def __neurodesc(cls, text, text_message):
        pass

    @classmethod
    def monitor(cls):
        pass

class TestMonitorLSTM(TestMonitor):

    def __init__(self):
        pass

    @classmethod
    def __emotionsrecognition(cls, text):
        return super()._emotionsrecognition(text)

    @classmethod
    def __neurodesc(cls, idx, text, text_message):

        emotion = ''

        #emotion = cls.__emotionsrecognition(text)

        b_predictor = super()._bpred.predict(text, super()._mapa.BUSINESSMAPA,
                                             './models/binary/LSTM/businessmodel.h5',
                                             './tokenizers/binary/LSTM/businesstokenizer.pickle',
                                             '')
        w_predictor = super()._bpred.predict(text, super()._mapa.WEATHERMAPA, './models/binary/LSTM/weathermodel.h5',
                                             './tokenizers/binary/LSTM/weathertokenizer.pickle',
                                             '')

        hi_predictor = super()._bpred.predict(text, super()._mapa.HIMAPA,
                                              './models/binary/LSTM/himodel.h5',
                                              './tokenizers/binary/LSTM/hitokenizer.pickle',
                                              '')
        th_predictor = super()._bpred.predict(text, super()._mapa.THMAPA,
                                              './models/binary/LSTM/thmodel.h5',
                                              './tokenizers/binary/LSTM/thtokenizer.pickle',
                                              '')
        return super()._decision(text_message, emotion, b_predictor, w_predictor, hi_predictor, th_predictor)

    @classmethod
    def monitor(cls):
        DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets."markedvalidsetLSTM" ml')

        df = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text from validation_sets."markedvalidsetHuman" mh ORDER BY id ASC')
        i = 0
        inptext = df['text']
        text = []

        for txt in inptext:
            idx = df['id'][i]
            tstr = txt.replace('миса', '')
            ststr = tstr.replace('misa', '')
            text.append(ststr)
            outlist = cls.__neurodesc(idx, text, ststr)
            outstr = ''
            if (outlist != None):
                for outmes in outlist:
                    outstr += outmes

            DB_Bridge.DB_Communication.insert_to(idx, ststr, outstr, 'markedvalidsetLSTM')
            text = []
            i = i + 1

class TestMonitorNaiveBayes(TestMonitor):

    def __init__(self):
        pass

    @classmethod
    def __emotionsrecognition(cls, text):
        emotion = super()._nnpred.predict(text, super()._mapa.EMOTIONSMAPA,
                                          './models/multy/NaiveBayes/emotionsmodel.pickle',
                                          './tokenizers/multy/NaiveBayes/emotionsvec.pickle', '')
        return emotion

    @classmethod
    def __neurodesc(cls, idx, text, text_message):

        emotion = ''

        b_predictor = super()._nnpred.predict(text, super()._mapa.BUSINESSMAPA,
                                              './models/binary/NaiveBayes/businessmodel.pickle',
                                              './tokenizers/binary/NaiveBayes/businessvec.pickle',
                                              '')

        w_predictor = super()._nnpred.predict(text, super()._mapa.WEATHERMAPA,
                                              './models/binary/NaiveBayes/weathermodel.pickle',
                                              './tokenizers/binary/NaiveBayes/weathervec.pickle',
                                              '')

        hi_predictor = super()._nnpred.predict(text, super()._mapa.HIMAPA,
                                               './models/binary/NaiveBayes/himodel.pickle',
                                               './tokenizers/binary/NaiveBayes/hivec.pickle',
                                               '')
        th_predictor = super()._nnpred.predict(text, super()._mapa.THMAPA,
                                               './models/binary/NaiveBayes/thmodel.pickle',
                                               './tokenizers/binary/NaiveBayes/thvec.pickle',
                                               '')

        return super()._decision(text_message, emotion, b_predictor, w_predictor, hi_predictor, th_predictor)

    @classmethod
    def monitor(cls):
        DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets."markedvalidsetNaiveBayes" mnb')

        df = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text from validation_sets."markedvalidsetHuman" mh ORDER BY id ASC')
        i = 0
        inptext = df['text']
        text = []

        for txt in inptext:
            idx = df['id'][i]
            tstr = txt.replace('миса', '')
            ststr = tstr.replace('misa', '')
            text.append(ststr)
            outlist = cls.__neurodesc(idx, text, ststr)
            outstr = ''
            if (outlist != None):
                for outmes in outlist:
                    outstr += outmes

            DB_Bridge.DB_Communication.insert_to(idx, ststr, outstr, 'markedvalidsetNaiveBayes')
            text = []
            i = i + 1

class TestMonitorRandomForest(TestMonitor):

    def __init__(self):
        pass

    @classmethod
    def __emotionsrecognition(cls, text):
        emotion = super()._rfpred.predict(text, super()._mapa.EMOTIONSMAPA,
                                          './models/multy/RandomForest/emotionsmodel.pickle',
                                          './tokenizers/multy/RandomForest/emotionsencoder.pickle', '')

        return emotion

    @classmethod
    def __neurodesc(cls, idx, text, text_message):

        #emotion = cls.__emotionsrecognition(text)
        emotion = ''

        b_predictor = super()._rfpred.predict(text, super()._mapa.BUSINESSMAPA,
                                              './models/binary/RandomForest/businessmodel.pickle',
                                              './tokenizers/binary/RandomForest/businessencoder.pickle',
                                              '')

        w_predictor = super()._rfpred.predict(text, super()._mapa.WEATHERMAPA,
                                              './models/binary/RandomForest/weathermodel.pickle',
                                              './tokenizers/binary/RandomForest/weatherencoder.pickle',
                                              '')

        hi_predictor = super()._rfpred.predict(text, super()._mapa.HIMAPA,
                                               './models/binary/RandomForest/himodel.pickle',
                                               './tokenizers/binary/RandomForest/hiencoder.pickle', '')

        th_predictor = super()._rfpred.predict(text, super()._mapa.THMAPA,
                                               './models/binary/RandomForest/thmodel.pickle',
                                               './tokenizers/binary/RandomForest/thencoder.pickle', '')

        return super()._decision(text_message, emotion, b_predictor, w_predictor, hi_predictor, th_predictor)

    @classmethod
    def monitor(cls):
        DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets."markedvalidsetRandomForest" mrf')

        df = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text from validation_sets."markedvalidsetHuman" mh ORDER BY id ASC')
        i = 0
        inptext = df['text']
        text = []

        for txt in inptext:
            idx = df['id'][i]
            tstr = txt.replace("миса", '')
            ststr = tstr.replace("misa", '')
            text.append(ststr)
            outlist = cls.__neurodesc(idx, text, ststr)
            outstr = ''
            if (outlist != None):
                for outmes in outlist:
                    outstr += outmes

            DB_Bridge.DB_Communication.insert_to(idx, ststr, outstr, 'markedvalidsetRandomForest')
            text = []
            i = i + 1
