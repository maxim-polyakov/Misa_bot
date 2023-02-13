from pathlib import Path
from Deep_layer.NLP_package.Models.Multy import MultyLSTM
from Deep_layer.NLP_package.Models.Binary import BinaryLSTM
from Core_layer.Bot_package import Selects
from Core_layer.Bot_package.Bototrainers import ITrainer


class LSTMtrain(ITrainer.ITrainer):
    sel = Selects.Select()
    @classmethod
    def hitrain(cls, epochs):
        filemodel = next(Path().rglob('0_himodel.h5'))
        filetokenizer = next(Path().rglob('0_hitokenizer.pickle'))
        datasetfile = cls.sel.SELECT_HI
        trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('hi', 'train', epochs)

    @classmethod
    def thtrain(cls, epochs):
        filemodel = next(Path().rglob('1_thmodel.h5'))
        filetokenizer = next(Path().rglob('1_thtokenizer.pickle'))
        datasetfile = cls.sel.SELECT_TH
        trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('thanks', 'train', epochs)

    @classmethod
    def businesstrain(cls, epochs):
        filemodel = next(Path().rglob('2_businessmodel.h5'))
        filetokenizer = next(Path().rglob('2_businesstokenizer.pickle'))
        datasetfile = cls.sel.SELECT_BUSINESS
        trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('business', 'train', epochs)

    @classmethod
    def weathertrain(cls, epochs):
        filemodel = next(Path().rglob('3_weathermodel.h5'))
        filetokenizer = next(Path().rglob('3_weathertokenizer.pickle'))
        datasetfile = cls.sel.SELECT_WEATHER
        trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('weather', 'train', epochs)

    @classmethod
    def emotionstrain(cls, epochs):
        filemodel = next(Path().rglob('0_emotionsmodel.h5'))
        filetokenizer = next(Path().rglob('0_emotionstokenizer.pickle'))
        datasetfile = cls.sel.SELECT_EMOTIONS
        trainer = MultyLSTM.MultyLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('emotionid', 7, 'train', epochs)

    @classmethod
    def trashtrain(cls, epochs):
        filemodel = next(Path().rglob('4_trashmodel.h5'))
        filetokenizer = next(Path().rglob('4_trashtokenizer.pickle'))
        datasetfile = cls.sel.SELECT_TRASH
        trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
        trainer.train('trash', 'train', epochs)