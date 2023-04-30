from pathlib import Path
from Deep_layer.NLP_package.Models.Multy import NaiveBayes
from Core_layer.Bot_package import Selects
from Core_layer.Bot_package.Bototrainers import ITrainer

class NBTrain(ITrainer.ITrainer):

    sel = Selects.Select()

    @classmethod
    def hitrain(cls):
        filemodel = next(Path().rglob('0_nbhimodel.pickle'))
        filetokenizer = next(Path().rglob('0_nbhiencoder.pickle'))
        datasetfile = cls.sel.SELECT_HI

        trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile)
        trainer.train('hi')

    @classmethod
    def thtrain(cls):
        filemodel = next(Path().rglob('1_nbthmodel.pickle'))
        filetokenizer = next(Path().rglob('1_nbthencoder.pickle'))

        datasetfile = cls.sel.SELECT_TH

        trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile)
        trainer.train('thanks')

    @classmethod
    def businesstrain(cls):
        filemodel = next(Path().rglob('2_nbbusinessmodel.pickle'))
        filetokenizer = next(Path().rglob('2_nbbusinessencoder.pickle'))

        datasetfile = cls.sel.SELECT_BUSINESS

        trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile,)
        trainer.train('business')

    @classmethod
    def weathertrain(cls):
        filemodel = next(Path().rglob('3_nbweathermodel.pickle'))
        filetokenizer = next(Path().rglob('3_nbweatherencoder.pickle'))
        datasetfile = cls.sel.SELECT_WEATHER

        trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile)
        trainer.train('weather')

    @classmethod
    def trashtrain(cls):
        filemodel = next(Path().rglob('4_nbtrashmodel.pickle'))
        filetokenizer = next(Path().rglob('4_nbtrashencoder.pickle'))

        datasetfile = cls.sel.SELECT_TRASH

        trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile)
        trainer.train('trash')

    @classmethod
    def emotionstrain(cls):
        filemodel = next(Path().rglob('0_nbemotionsmodel.pickle'))
        filetokenizer = next(Path().rglob('0_nbemotionsencoder.pickle'))

        datasetfile = cls.sel.SELECT_EMOTIONS

        trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile)
        trainer.train('emotionid')
