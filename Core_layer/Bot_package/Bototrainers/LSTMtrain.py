from pathlib import Path
from Deep_layer.NLP_package.Models.Multy import MultyLSTM
from Deep_layer.NLP_package.Models.Binary import BinaryLSTM
from Core_layer.Bot_package import Selects
from Core_layer.Bot_package.Bototrainers import ITrainer


class LSTMtrain(ITrainer.ITrainer):

    sel = Selects.Select()

    @classmethod
    def hitrain(cls, epochs):
#
#
        try:
            filemodel = next(Path().rglob('0_lstmhimodel.h5'))
            filetokenizer = next(Path().rglob('0_lstmhitokenizer.pickle'))
            datasetfile = cls.sel.SELECT_HI
            trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
            trainer.train('hi', epochs)
        except:
            pass
    @classmethod
    def thtrain(cls, epochs):
#
#
        try:
            filemodel = next(Path().rglob('1_lstmthmodel.h5'))
            filetokenizer = next(Path().rglob('1_lstmthtokenizer.pickle'))
            datasetfile = cls.sel.SELECT_TH
            trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
            trainer.train('thanks', epochs)
        except:
            pass

    @classmethod
    def businesstrain(cls, epochs):
#
#
        try:
            filemodel = next(Path().rglob('2_lstmbusinessmodel.h5'))
            filetokenizer = next(Path().rglob('2_lstmbusinesstokenizer.pickle'))
            datasetfile = cls.sel.SELECT_BUSINESS
            trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
            trainer.train('business', epochs)
        except:
            pass

    @classmethod
    def weathertrain(cls, epochs):
#
#
        try:
            filemodel = next(Path().rglob('3_lstmweathermodel.h5'))
            filetokenizer = next(Path().rglob('3_lstmweathertokenizer.pickle'))
            datasetfile = cls.sel.SELECT_WEATHER
            trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
            trainer.train('weather', epochs)
        except:
            pass

    @classmethod
    def trashtrain(cls, epochs):
#
#
        try:
            filemodel = next(Path().rglob('4_lstmtrashmodel.h5'))
            filetokenizer = next(Path().rglob('4_lstmtrashtokenizer.pickle'))
            datasetfile = cls.sel.SELECT_TRASH
            trainer = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
            trainer.train('trash', epochs)
        except:
            pass

    @classmethod
    def emotionstrain(cls, epochs):
#
#
            filemodel = next(Path().rglob('0_lstmemotionsmodel.h5'))
            filetokenizer = next(Path().rglob('0_lstmemotionstokenizer.pickle'))
            datasetfile = cls.sel.SELECT_EMOTIONS
            trainer = MultyLSTM.MultyLSTM(filemodel, filetokenizer, datasetfile)
            trainer.train('emotionid', 7, epochs)



