from Core_layer import Test_package


class ITestMonitor(Test_package.ABC):

    @Test_package.abstractmethod
    def monitor(self):
        pass

class TestMonitor(ITestMonitor):
    _bpred = Test_package.Predictors.BinaryLSTM()
    _nnpred = Test_package.Predictors.NaiveBayes()
    _rfpred = Test_package.Predictors.RandomForest()
    _mpred = Test_package.Predictors.MultyLSTM()
    _xgpred = Test_package.Predictors.Xgboost()

    _pr = Test_package.TextPreprocessers.CommonPreprocessing()

    _dbc = Test_package.DB_Bridge.DB_Communication()

    _be = Test_package.Botoevaluaters.Binaryevaluate()
    _me = Test_package.Botoevaluaters.Multyevaluate()
    _mapa = Test_package.Mapas.Mapa()

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
        Test_package.DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets."markedvalidsetLSTM" ml')

        df = Test_package.DB_Bridge.DB_Communication.get_data(
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

            Test_package.DB_Bridge.DB_Communication.insert_to(idx, ststr, outstr, 'markedvalidsetLSTM')
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
        Test_package.DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets."markedvalidsetNaiveBayes" mnb')

        df = Test_package.DB_Bridge.DB_Communication.get_data(
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

            Test_package.DB_Bridge.DB_Communication.insert_to(idx, ststr, outstr, 'markedvalidsetNaiveBayes')
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
        Test_package.DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets."markedvalidsetRandomForest" mrf')

        df = Test_package.DB_Bridge.DB_Communication.get_data(
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

            Test_package.DB_Bridge.DB_Communication.insert_to(idx, ststr, outstr, 'markedvalidsetRandomForest')
            text = []
            i = i + 1

class TestMonitorXGBoost(TestMonitor):

    def __init__(self):
        pass

    @classmethod
    def __emotionsrecognition(cls, text):
        emotion = super()._xgpred.predict(text, super()._mapa.EMOTIONSMAPA,
                                          './models/multy/Xgboost/emotionsmodel.pickle',
                                          './tokenizers/multy/Xgboost/emotionstokenizer.pickle', '')

        return emotion

    @classmethod
    def __neurodesc(cls, idx, text, text_message):

       #emotion = cls.__emotionsrecognition(text)
        emotion = ''
        b_predictor = super()._xgpred.predict(text, super()._mapa.BUSINESSMAPA,
                                              './models/binary/Xgboost/businessmodel.pickle',
                                              './tokenizers/binary/Xgboost/businesstokenizer.pickle',
                                              '')

        w_predictor = super()._xgpred.predict(text, super()._mapa.WEATHERMAPA,
                                              './models/binary/Xgboost/weathermodel.pickle',
                                              './tokenizers/binary/Xgboost/weathertokenizer.pickle',
                                              '')

        hi_predictor = super()._xgpred.predict(text, super()._mapa.HIMAPA,
                                               './models/binary/Xgboost/himodel.pickle',
                                               './tokenizers/binary/Xgboost/hitokenizer.pickle', '')

        th_predictor = super()._xgpred.predict(text, super()._mapa.THMAPA,
                                               './models/binary/Xgboost/thmodel.pickle',
                                               './tokenizers/binary/Xgboost/thtokenizer.pickle', '')

        return super()._decision(text_message, emotion, b_predictor, w_predictor, hi_predictor, th_predictor)

    @classmethod
    def monitor(cls):
        Test_package.DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets."markedvalidsetXGBoost" mx')

        df = Test_package.DB_Bridge.DB_Communication.get_data(
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

            Test_package.DB_Bridge.DB_Communication.insert_to(idx, ststr, outstr, 'markedvalidsetXGBoost')
            text = []
            i = i + 1

class TestMonitorCombine(TestMonitor):

    def __init__(self):
        pass

    @classmethod
    def __emotionsrecognition(cls, text):
        return super(TestMonitorCombine, cls)._emotionsrecognition(text)

    @classmethod
    def __neurodesc(cls, idx, text, text_message):

        #emotion = cls.__emotionsrecognition(text)
        emotion = ''
        compred = Test_package.Predictors.CombineModelBinary('./models/binary/NaiveBayes/businessmodel.pickle',
                                                             './tokenizers/binary/NaiveBayes/businessvec.pickle',
                                                             './models/binary/RandomForest/businessmodel.pickle',
                                                             './tokenizers/binary/RandomForest/businessencoder.pickle',
                                                             './models/binary/LSTM/businessmodel.h5',
                                                             './tokenizers/binary/LSTM/businesstokenizer.pickle',
                                                             './models/binary/Xgboost/businessmodel.pickle',
                                                             './tokenizers/binary/Xgboost/businesstokenizer.pickle')

        b_predictor = compred.predict(text, super()._mapa.BUSINESSMAPA)

        compred = Test_package.Predictors.CombineModelBinary('./models/binary/NaiveBayes/weathermodel.pickle',
                                                             './tokenizers/binary/NaiveBayes/weathervec.pickle',
                                                             './models/binary/RandomForest/weathermodel.pickle',
                                                             './tokenizers/binary/RandomForest/weatherencoder.pickle',
                                                             './models/binary/LSTM/weathermodel.h5',
                                                             './tokenizers/binary/LSTM/weathertokenizer.pickle',
                                                             './models/binary/Xgboost/weathermodel.pickle',
                                                             './tokenizers/binary/Xgboost/weathertokenizer.pickle')

        w_predictor = compred.predict(text, super()._mapa.WEATHERMAPA)

        compred = Test_package.Predictors.CombineModelBinary('./models/binary/NaiveBayes/himodel.pickle',
                                                             './tokenizers/binary/NaiveBayes/hivec.pickle',
                                                             './models/binary/RandomForest/himodel.pickle',
                                                             './tokenizers/binary/RandomForest/hiencoder.pickle',
                                                             './models/binary/LSTM/himodel.h5',
                                                             './tokenizers/binary/LSTM/hitokenizer.pickle',
                                                             './models/binary/Xgboost/himodel.pickle',
                                                             './tokenizers/binary/Xgboost/hitokenizer.pickle')

        hi_predictor = compred.predict(text, super()._mapa.HIMAPA)

        compred = Test_package.Predictors.CombineModelBinary('./models/binary/NaiveBayes/thmodel.pickle',
                                                             './tokenizers/binary/NaiveBayes/thvec.pickle',
                                                             './models/binary/RandomForest/thmodel.pickle',
                                                             './tokenizers/binary/RandomForest/thencoder.pickle',
                                                             './models/binary/LSTM/thmodel.h5',
                                                             './tokenizers/binary/LSTM/thtokenizer.pickle',
                                                             './models/binary/Xgboost/thmodel.pickle',
                                                             './tokenizers/binary/Xgboost/thtokenizer.pickle')

        th_predictor = compred.predict(text, super()._mapa.THMAPA)

        return super()._decision(text_message, emotion, b_predictor, w_predictor, hi_predictor, th_predictor)

    @classmethod
    def monitor(cls):
        Test_package.DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets."markedvalidsetCombine" mc ')

        df = Test_package.DB_Bridge.DB_Communication.get_data(
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

            Test_package.DB_Bridge.DB_Communication.insert_to(idx, ststr, outstr, 'markedvalidsetCombine')
            text = []
            i = i + 1
