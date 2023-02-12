from pathlib import Path
from Deep_layer.NLP_package import Models
from abc import ABC, abstractmethod
from Core_layer.Bot_package import Selects

class ITrainer(ABC):
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

class LSTMtrain(ITrainer):
    sel = Selects.Select()
    @classmethod
    def hitrain(cls, epochs):
        filemodel = next(Path().rglob('0_himodel.h5'))
        filetokenizer = next(Path().rglob('0_hitokenizer.pickle'))
        datasetfile = cls.sel.SELECT_HI
        trainer = Models.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('hi', 'train', epochs)

    @classmethod
    def thtrain(cls, epochs):
        filemodel = next(Path().rglob('1_thmodel.h5'))
        filetokenizer = next(Path().rglob('1_thtokenizer.pickle'))
        datasetfile = cls.sel.SELECT_TH
        trainer = Models.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('thanks', 'train', epochs)

    @classmethod
    def businesstrain(cls, epochs):
        filemodel = next(Path().rglob('2_businessmodel.h5'))
        filetokenizer = next(Path().rglob('2_businesstokenizer.pickle'))
        datasetfile = cls.sel.SELECT_BUSINESS
        trainer = Models.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('business', 'train', epochs)

    @classmethod
    def weathertrain(cls, epochs):
        filemodel = next(Path().rglob('3_weathermodel.h5'))
        filetokenizer = next(Path().rglob('3_weathertokenizer.pickle'))
        datasetfile = cls.sel.SELECT_WEATHER
        trainer = Models.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('weather', 'train', epochs)

    @classmethod
    def emotionstrain(cls, epochs):
        filemodel = next(Path().rglob('emotionsmodel.h5'))
        filetokenizer = next(Path().rglob('emotionstokenizer.pickle'))
        datasetfile = cls.sel.SELECT_EMOTIONS
        trainer = Models.MultyLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('emotionid', 7, 'train', epochs)

    @classmethod
    def trashtrain(cls, epochs):
        filemodel = next(Path().rglob('4_trashmodel.h5'))
        filetokenizer = next(Path().rglob('4_trashtokenizer.pickle'))
        datasetfile = cls.sel.SELECT_TRASH
        trainer = Models.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('trash', 'train', epochs)