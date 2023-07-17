from pathlib import Path
from Deep_layer.NLP_package.Models.Multy import XGBClassifier
from Core_layer.Bot_package.Classes import Selects
from Core_layer.Bot_package.Interfaces import ITrainer


class XGBtrain(ITrainer.ITrainer):

    sel = Selects.Select()

    @classmethod
    def hitrain(cls):
#
#
        try:
            filemodel = next(Path().rglob('0_xgbhimodel.pickle'))
            filetokenizer = next(Path().rglob('0_xgbhiencoder.pickle'))
            datasetfile = cls.sel.SELECT_HI

            trainer = XGBClassifier.XGBClassifier(filemodel, filetokenizer, datasetfile)
            trainer.train('hi')
        except:
            pass

    @classmethod
    def thtrain(cls):
        try:
            filemodel = next(Path().rglob('1_xgbthmodel.pickle'))
            filetokenizer = next(Path().rglob('1_xgbthencoder.pickle'))

            datasetfile = cls.sel.SELECT_TH

            trainer = XGBClassifier.XGBClassifier(filemodel, filetokenizer, datasetfile)
            trainer.train('thanks')
        except:
            pass

    @classmethod
    def businesstrain(cls):
        try:
            filemodel = next(Path().rglob('2_xgbbusinessmodel.pickle'))
            filetokenizer = next(Path().rglob('2_xgbbusinessencoder.pickle'))

            datasetfile = cls.sel.SELECT_BUSINESS

            trainer = XGBClassifier.XGBClassifier(filemodel, filetokenizer, datasetfile,)
            trainer.train('business')
        except:
            pass

    @classmethod
    def weathertrain(cls):
        try:
            filemodel = next(Path().rglob('3_xgbweathermodel.pickle'))
            filetokenizer = next(Path().rglob('3_xgbweatherencoder.pickle'))
            datasetfile = cls.sel.SELECT_WEATHER

            trainer = XGBClassifier.XGBClassifier(filemodel, filetokenizer, datasetfile)
            trainer.train('weather')
        except:
            pass

    @classmethod
    def trashtrain(cls):
        try:
            filemodel = next(Path().rglob('4_xgbtrashmodel.pickle'))
            filetokenizer = next(Path().rglob('4_xgbtrashencoder.pickle'))

            datasetfile = cls.sel.SELECT_TRASH

            trainer = XGBClassifier.XGBClassifier(filemodel, filetokenizer, datasetfile)
            trainer.train('trash')
        except:
            pass

    @classmethod
    def emotionstrain(cls):
        try:
            filemodel = next(Path().rglob('0_xgbemotionsmodel.pickle'))
            filetokenizer = next(Path().rglob('0_xgbemotionsencoder.pickle'))

            datasetfile = cls.sel.SELECT_EMOTIONS

            trainer = XGBClassifier.XGBClassifier(filemodel, filetokenizer, datasetfile)
            trainer.train('emotionid')
        except:
            pass


