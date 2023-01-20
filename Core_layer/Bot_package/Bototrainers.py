from Core_layer import Bot_package
from Deep_layer import NLP_package


class ITrain(Bot_package.ABC):
    @Bot_package.abstractmethod
    def hitrain(cls):
        pass
    @Bot_package.abstractmethod
    def thtrain(cls):
        pass
    @Bot_package.abstractmethod
    def businesstrain(cls):
        pass
    @Bot_package.abstractmethod
    def weathertrain(cls):
        pass
    @Bot_package.abstractmethod
    def emotionstrain(cls):
        pass
    @Bot_package.abstractmethod
    def trashtrain(cls):
        pass

class LSTMtrain(ITrain):

    sel = Bot_package.Selects.Select()

    @classmethod
    def hitrain(cls, epochs):
        filemodel = next(Bot_package.Path().rglob('himodel.h5'))
        filetokenizer = next(Bot_package.Path().rglob('hitokenizer.pickle'))
        datasetfile = cls.sel.SELECT_HI
        recognizeddata = 'SELECT text, hi FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (hi=0 or hi=1) ORDER BY random() LIMIT 3000'
        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)

        trainer.train('hi', 'train', epochs)
    @classmethod
    def thtrain(cls, epochs):
        filemodel = next(Bot_package.Path().rglob('thmodel.h5'))
        filetokenizer = next(Bot_package.Path().rglob('thtokenizer.pickle'))
        datasetfile = cls.sel.SELECT_TH
        recognizeddata = 'SELECT text, thanks FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (thanks=0 or thanks=1) ORDER BY random() LIMIT 3000'

        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)

        trainer.train('thanks', 'train', epochs)
    @classmethod
    def businesstrain(cls, epochs):
        filemodel = next(Bot_package.Path().rglob('businessmodel.h5'))
        filetokenizer = next(Bot_package.Path().rglob('businesstokenizer.pickle'))
        datasetfile = cls.sel.SELECT_BUSINESS
        recognizeddata = 'SELECT text, business FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (business=0 or business=1) ORDER BY random() LIMIT 3000'

        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)

        trainer.train('business', 'train', epochs)
    @classmethod
    def weathertrain(cls, epochs):
        filemodel = next(Bot_package.Path().rglob('weathermodel.h5'))
        filetokenizer = next(Bot_package.Path().rglob('weathertokenizer.pickle'))
        datasetfile = cls.sel.SELECT_WEATHER
        recognizeddata = 'SELECT text, weather FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (weather=0 or weather=1) ORDER BY random() LIMIT 3000'

        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)

        trainer.train('weather', 'train', epochs)
    @classmethod
    def emotionstrain(cls, epochs):
        filemodel = next(Bot_package.Path().rglob('emotionsmodel.h5'))
        filetokenizer = next(Bot_package.Path().rglob('emotionstokenizer.pickle'))
        datasetfile = cls.sel.SELECT_EMOTIONS
        recognizeddata = 'SELECT text, emotionid FROM recognized_sets.recognized_all_set'
        trainer = Bot_package.Models.MultyLSTM(filemodel, filetokenizer,
                                               datasetfile, recognizeddata)

        trainer.train('emotionid', 7, 'train', epochs)
    @classmethod
    def trashtrain(cls, epochs):
        filemodel = next(Bot_package.Path().rglob('trashmodel.h5'))
        filetokenizer = next(Bot_package.Path().rglob('trashtokenizer.pickle'))
        datasetfile = cls.sel.SELECT_TRASH
        recognizeddata = 'SELECT text, emotionid FROM recognized_sets.recognized_all_set'

        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)

        trainer.train('trash', 'train', epochs)

class NaiveBayesTrain(ITrain):

    sel = Bot_package.Selects.Select()

    @classmethod
    def hitrain(cls):
        filemodel = './models/binary/NaiveBayes/himodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/hivec.pickle'

        datasetfile = cls.sel.SELECT_HI

        recognizeddata = 'SELECT text, hi FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (hi=0 or hi=1) ORDER BY random() LIMIT 3000'
        trainer = Bot_package.Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)
        trainer.train('hi', 'train')
    @classmethod
    def thtrain(cls):
        filemodel = './models/binary/NaiveBayes/thmodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/thvec.pickle'
        datasetfile = cls.sel.SELECT_TH
        recognizeddata = 'SELECT text, thanks FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (thanks=0 or thanks=1) ORDER BY random() LIMIT 3000'

        trainer = Bot_package.Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('thanks', 'train')
    @classmethod
    def businesstrain(cls):
        filemodel = './models/binary/NaiveBayes/businessmodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/businessvec.pickle'
        datasetfile = cls.sel.SELECT_BUSINESS
        recognizeddata = 'SELECT text, business FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (business=0 or business=1) ORDER BY random() LIMIT 3000'

        trainer = Bot_package.Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('business', 'train')
    @classmethod
    def weathertrain(cls):
        filemodel = './models/binary/NaiveBayes/weathermodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/weathervec.pickle'
        datasetfile = cls.sel.SELECT_WEATHER
        recognizeddata = 'SELECT text, weather FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (weather=0 or weather=1) ORDER BY random() LIMIT 3000'

        trainer = Bot_package.Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('weather', 'train')
    @classmethod
    def emotionstrain(cls):
        filemodel = './models/multy/NaiveBayes/emotionsmodel.pickle'
        filetokenizer = './tokenizers/multy/NaiveBayes/emotionsvec.pickle'
        datasetfile = cls.sel.SELECT_EMOTIONS
        recognizeddata = 'SELECT text, emotionid FROM recognized_sets.recognized_all_set'


        trainer = Bot_package.Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('emotionid', 'train')
    @classmethod
    def trashtrain(cls):
        pass

class RandomForestTrain(ITrain):

    sel = Bot_package.Selects.Select()

    @classmethod
    def hitrain(cls):
        filemodel = './models/binary/RandomForest/himodel.pickle'
        filetokenizer = './tokenizers/binary/RandomForest/hiencoder.pickle'
        datasetfile = cls.sel.SELECT_HI
        recognizeddata = 'SELECT text, hi FROM recognized_sets.recognized_all_set WHERE' + \
                         ' (hi=0 or hi=1) ORDER BY random() LIMIT 3000'

        trainer = NLP_package.Models.RandomForest(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('hi', 'train')
    @classmethod
    def thtrain(cls):
        filemodel = './models/binary/RandomForest/thmodel.pickle'
        filetokenizer = './tokenizers/binary/RandomForest/thencoder.pickle'
        datasetfile = cls.sel.SELECT_TH
        recognizeddata = 'SELECT text, thanks FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (thanks=0 or thanks=1) ORDER BY random() LIMIT 3000'

        trainer = NLP_package.Models.RandomForest(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('thanks', 'train')
    @classmethod
    def businesstrain(cls):
        filemodel = './models/binary/RandomForest/businessmodel.pickle'
        filetokenizer = './tokenizers/binary/RandomForest/businessencoder.pickle'
        datasetfile = cls.sel.SELECT_BUSINESS
        recognizeddata = 'SELECT text, business FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (business=0 or business=1) ORDER BY random() LIMIT 3000'

        trainer = Bot_package.Models.RandomForest(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('business', 'train')
    @classmethod
    def weathertrain(cls):
        filemodel = './models/binary/RandomForest/weathermodel.pickle'
        filetokenizer = './tokenizers/binary/RandomForest/weatherencoder.pickle'
        datasetfile = cls.sel.SELECT_WEATHER
        recognizeddata = 'SELECT text, weather FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (weather=0 or weather=1) ORDER BY random() LIMIT 3000'

        trainer = Bot_package.Models.RandomForest(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('weather', 'train')
    @classmethod
    def emotionstrain(cls):
        filemodel = './models/multy/RandomForest/emotionsmodel.pickle'
        filetokenizer = './tokenizers/multy/RandomForest/emotionsencoder.pickle'
        datasetfile = cls.sel.SELECT_EMOTIONS
        recognizeddata = 'SELECT text, emotionid FROM recognized_sets.recognized_emotionstrain'

        trainer = Bot_package.Models.RandomForest(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('emotionid', 'train')
    @classmethod
    def trashtrain(cls):
        pass

class XgboostTrain(ITrain):

    sel = Bot_package.Selects.Select()

    @classmethod
    def hitrain(cls):
        filemodel = './models/binary/Xgboost/himodel.pickle'
        filetokenizer = './tokenizers/binary/Xgboost/hitokenizer.pickle'
        datasetfile = cls.sel.SELECT_HI
        recognizeddata = 'SELECT text, hi FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (hi=0 or hi=1) ORDER BY random() LIMIT 3000'

        trainer = NLP_package.Models.XGBClassifier(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('hi', 'train')
    @classmethod
    def thtrain(cls):
        filemodel = './models/binary/Xgboost/thmodel.pickle'
        filetokenizer = './tokenizers/binary/Xgboost/thtokenizer.pickle'
        datasetfile = cls.sel.SELECT_TH
        recognizeddata = 'SELECT text, thanks FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (thanks=0 or thanks=1) ORDER BY random() LIMIT 3000'

        trainer = NLP_package.Models.XGBClassifier(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('thanks', 'train')
    @classmethod
    def businesstrain(cls):
        filemodel = './models/binary/Xgboost/businessmodel.pickle'
        filetokenizer = './tokenizers/binary/Xgboost/businesstokenizer.pickle'
        datasetfile = cls.sel.SELECT_BUSINESS
        recognizeddata = 'SELECT text, business FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (business=0 or business=1) ORDER BY random() LIMIT 3000'

        trainer = NLP_package.Models.XGBClassifier(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('business', 'train')
    @classmethod
    def weathertrain(cls):
        filemodel = './models/binary/Xgboost/weathermodel.pickle'
        filetokenizer = './tokenizers/binary/Xgboost/weathertokenizer.pickle'
        datasetfile = cls.sel.SELECT_WEATHER
        recognizeddata = 'SELECT text, weather FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (weather=0 or weather=1) ORDER BY random() LIMIT 3000'

        trainer = Bot_package.Models.XGBClassifier(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('weather', 'train')
    @classmethod
    def emotionstrain(cls):
        filemodel = './models/multy/Xgboost/emotionsmodel.pickle'
        filetokenizer = './tokenizers/multy/Xgboost/emotionstokenizer.pickle'
        datasetfile = cls.sel.SELECT_EMOTIONS
        recognizeddata = 'SELECT text, emotionid FROM recognized_sets.recognized_all_set'

        trainer = Bot_package.Models.XGBClassifier(filemodel, filetokenizer, datasetfile, recognizeddata)

        trainer.train('emotionid', 'train')
    @classmethod
    def trashtrain(cls):
        pass