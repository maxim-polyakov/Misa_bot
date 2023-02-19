from pathlib import Path
from Deep_layer.NLP_package.Models.Multy import RandomForest
from Core_layer.Bot_package import Selects
from Core_layer.Bot_package.Bototrainers import ITrainer


class RFtrain(ITrainer.ITrainer):

    sel = Selects.Select()

    @classmethod
    def hitrain(cls):
        filemodel = next(Path().rglob('0_rfhimodel.pickle'))
        filetokenizer = next(Path().rglob('0_rfhiencoder.pickle'))
        datasetfile = cls.sel.SELECT_HI

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('hi')

    @classmethod
    def thtrain(cls):
        filemodel = next(Path().rglob('1_rfthmodel.pickle'))
        filetokenizer = next(Path().rglob('1_rfthencoder.pickle'))

        datasetfile = cls.sel.SELECT_TH

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('thanks')

    @classmethod
    def businesstrain(cls):
        filemodel = next(Path().rglob('2_rfbusinessmodel.pickle'))
        filetokenizer = next(Path().rglob('2_rfbusinessencoder.pickle'))

        datasetfile = cls.sel.SELECT_BUSINESS

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile,)
        trainer.train('business')

    @classmethod
    def weathertrain(cls):
        filemodel = next(Path().rglob('3_rfweathermodel.pickle'))
        filetokenizer = next(Path().rglob('3_rfweatherencoder.pickle'))
        datasetfile = cls.sel.SELECT_WEATHER

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('weather')

    @classmethod
    def trashtrain(cls):
        filemodel = next(Path().rglob('4_rftrashmodel.pickle'))
        filetokenizer = next(Path().rglob('4_rftrashencoder.pickle'))

        datasetfile = cls.sel.SELECT_TRASH

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('trash')

    @classmethod
    def emotionstrain(cls):
        filemodel = next(Path().rglob('0_rfemotionsmodel.pickle'))
        filetokenizer = next(Path().rglob('0_rfemotionsencoder.pickle'))

        datasetfile = cls.sel.SELECT_EMOTIONS

        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('emotionid')


