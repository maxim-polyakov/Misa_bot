from pathlib import Path
from Deep_layer.NLP_package import Models
from Deep_layer import NLP_package
from abc import ABC, abstractmethod
from Core_layer.Bot_package import Selects

class ITrain(ABC):
    @abstractmethod
    def hitrain(cls):
        pass
    @abstractmethod
    def thtrain(cls):
        pass
    @abstractmethod
    def businesstrain(cls):
        pass
    @abstractmethod
    def weathertrain(cls):
        pass
    @abstractmethod
    def emotionstrain(cls):
        pass
    @abstractmethod
    def trashtrain(cls):
        pass

class LSTMtrain(ITrain):
    sel = Selects.Select()
    @classmethod
    def hitrain(cls, epochs):
        filemodel = next(Path().rglob('0_himodel.h5'))
        filetokenizer = next(Path().rglob('0_hitokenizer.pickle'))
        datasetfile = cls.sel.SELECT_HI
        recognizeddata = 'SELECT text, hi FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (hi=0 or hi=1) ORDER BY random() LIMIT 3000'
        trainer = Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)
        trainer.train('hi', 'train', epochs)

    @classmethod
    def thtrain(cls, epochs):
        filemodel = next(Path().rglob('1_thmodel.h5'))
        filetokenizer = next(Path().rglob('1_thtokenizer.pickle'))
        datasetfile = cls.sel.SELECT_TH
        recognizeddata = 'SELECT text, thanks FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (thanks=0 or thanks=1) ORDER BY random() LIMIT 3000'

        trainer = Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)

        trainer.train('thanks', 'train', epochs)

    @classmethod
    def businesstrain(cls, epochs):
        filemodel = next(Path().rglob('2_businessmodel.h5'))
        filetokenizer = next(Path().rglob('2_businesstokenizer.pickle'))
        datasetfile = cls.sel.SELECT_BUSINESS
        recognizeddata = 'SELECT text, business FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (business=0 or business=1) ORDER BY random() LIMIT 3000'
        trainer = Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)
        trainer.train('business', 'train', epochs)

    @classmethod
    def weathertrain(cls, epochs):
        filemodel = next(Path().rglob('3_weathermodel.h5'))
        filetokenizer = next(Path().rglob('3_weathertokenizer.pickle'))
        datasetfile = cls.sel.SELECT_WEATHER
        recognizeddata = 'SELECT text, weather FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (weather=0 or weather=1) ORDER BY random() LIMIT 3000'
        trainer = Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)
        trainer.train('weather', 'train', epochs)

    @classmethod
    def emotionstrain(cls, epochs):
        filemodel = next(Path().rglob('emotionsmodel.h5'))
        filetokenizer = next(Path().rglob('emotionstokenizer.pickle'))
        datasetfile = cls.sel.SELECT_EMOTIONS
        recognizeddata = 'SELECT text, emotionid FROM recognized_sets.recognized_all_set'
        trainer = Models.MultyLSTM(filemodel, filetokenizer,
                                               datasetfile, recognizeddata)
        trainer.train('emotionid', 7, 'train', epochs)

    @classmethod
    def trashtrain(cls, epochs):
        filemodel = next(Path().rglob('4_trashmodel.h5'))
        filetokenizer = next(Path().rglob('4_trashtokenizer.pickle'))
        datasetfile = cls.sel.SELECT_TRASH
        recognizeddata = 'SELECT text, emotionid FROM recognized_sets.recognized_all_set'
        trainer = Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)
        trainer.train('trash', 'train', epochs)

class NaiveBayesTrain(ITrain):
    sel = Selects.Select()
    @classmethod
    def hitrain(cls):
        filemodel = './models/binary/NaiveBayes/himodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/hivec.pickle'
        datasetfile = cls.sel.SELECT_HI
        recognizeddata = 'SELECT text, hi FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (hi=0 or hi=1) ORDER BY random() LIMIT 3000'
        trainer = Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)
        trainer.train('hi', 'train')

    @classmethod
    def thtrain(cls):
        filemodel = './models/binary/NaiveBayes/thmodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/thvec.pickle'
        datasetfile = cls.sel.SELECT_TH
        recognizeddata = 'SELECT text, thanks FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (thanks=0 or thanks=1) ORDER BY random() LIMIT 3000'
        trainer = Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)
        trainer.train('thanks', 'train')

    @classmethod
    def businesstrain(cls):
        filemodel = './models/binary/NaiveBayes/businessmodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/businessvec.pickle'
        datasetfile = cls.sel.SELECT_BUSINESS
        recognizeddata = 'SELECT text, business FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (business=0 or business=1) ORDER BY random() LIMIT 3000'
        trainer = Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)
        trainer.train('business', 'train')

    @classmethod
    def weathertrain(cls):
        filemodel = './models/binary/NaiveBayes/weathermodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/weathervec.pickle'
        datasetfile = cls.sel.SELECT_WEATHER
        recognizeddata = 'SELECT text, weather FROM recognized_sets.recognized_all_set WHERE ' + \
                         ' (weather=0 or weather=1) ORDER BY random() LIMIT 3000'
        trainer = Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)
        trainer.train('weather', 'train')

    @classmethod
    def emotionstrain(cls):
        filemodel = './models/multy/NaiveBayes/emotionsmodel.pickle'
        filetokenizer = './tokenizers/multy/NaiveBayes/emotionsvec.pickle'
        datasetfile = cls.sel.SELECT_EMOTIONS
        recognizeddata = 'SELECT text, emotionid FROM recognized_sets.recognized_all_set'
        trainer = Models.NaiveBayes(filemodel, filetokenizer, datasetfile, recognizeddata)
        trainer.train('emotionid', 'train')

    @classmethod
    def trashtrain(cls):
        pass
