from pathlib import Path
from Deep_layer.NLP_package.Models.Multy import RandomForest
from Core_layer.Bot_package import Selects
from Core_layer.Bot_package.Bototrainers import ITrainer


class RFtrain(ITrainer.ITrainer):

    sel = Selects.Select()

    @classmethod
    def hitrain(cls):
        filemodel = next(Path().rglob('0_himodel.pickle'))
        filetokenizer = next(Path().rglob('0_hiencoder.pickle'))
        datasetfile = cls.sel.SELECT_HI

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('hi')

    @classmethod
    def thtrain(cls):
        filemodel = next(Path().rglob('1_thmodel.pickle'))
        filetokenizer = next(Path().rglob('1_thencoder.pickle'))

        datasetfile = cls.sel.SELECT_TH

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('thanks')

    @classmethod
    def businesstrain(cls):
        filemodel = next(Path().rglob('2_businessmodel.pickle'))
        filetokenizer = next(Path().rglob('2_businessencoder.pickle'))

        datasetfile = cls.sel.SELECT_BUSINESS

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile,)
        trainer.train('business')

    @classmethod
    def weathertrain(cls):
        filemodel = next(Path().rglob('3_weathermodel.pickle'))
        filetokenizer = next(Path().rglob('3_weatherencoder.pickle'))
        datasetfile = cls.sel.SELECT_WEATHER

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('weather')

    @classmethod
    def trashtrain(cls):
        filemodel = next(Path().rglob('4_trashmodel.pickle'))
        filetokenizer = next(Path().rglob('4_trashencoder.pickle'))

        datasetfile = cls.sel.SELECT_TRASH

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('trash')

    @classmethod
    def emotionstrain(cls):
        filemodel = next(Path().rglob('0_emotionsmodel.pickle'))
        filetokenizer = next(Path().rglob('0_emotionsencoder.pickle'))

        datasetfile = cls.sel.SELECT_EMOTIONS

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('emotionid')


