from Core_layer import Bot_package as bp


class IEvaluate(bp.ABC):

    @bp.abstractmethod
    def hievaluate(cls):
        pass

    @bp.abstractmethod
    def quevaluate(cls):
        pass

    @bp.abstractmethod
    def thevaluate(cls):
        pass

    @bp.abstractmethod
    def commandevaluate(cls):
        pass

    @bp.abstractmethod
    def hi_th_commandevaluate(cls):
        pass

    @bp.abstractmethod
    def multyclassevaluate(cls):
        pass

    @bp.abstractmethod
    def emotionsevaluate(cls):
        pass

class Binaryevaluate(IEvaluate):

    @classmethod
    def hievaluate(cls):
        filemodel = './models/binary/LSTM/himodel.h5'
        filetokenizer = './tokenizers/binary/LSTM/hitokenizer.pickle'
        datasetfile = 'SELECT * FROM hiset'
        recognizeddata = 'SELECT * FROM recognized_hiset'
        trainer = bp.Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)
        trainer.train('hi', 'evaluate', 200)

    @classmethod
    def quevaluate(cls):
        filemodel = './models/binary/LSTM/qumodel.h5'
        filetokenizer = './tokenizers/binary/LSTM/qutokenizer.pickle'
        datasetfile = 'SELECT * FROM questionset'
        recognizeddata = 'SELECT * FROM recognized_questionset'
        trainer = bp.Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)
        trainer.train('question', 'evaluate', 200)

    @classmethod
    def thevaluate(cls):
        filemodel = './models/binary/LSTM/qumodel.h5'
        filetokenizer = './tokenizers/binary/LSTM/thtokenizer.pickle'
        datasetfile = 'SELECT * FROM thanksset'
        recognizeddata = 'SELECT * FROM recognized_thanksset'
        trainer = bp.Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)
        trainer.train('thanks', 'evaluate', 200)

    @classmethod
    def commandevaluate(cls):
        filemodel = './models/binary/commandmodel.h5'
        filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
        datasetfile = 'SELECT * FROM commandset'
        recognizeddata = 'SELECT * FROM recognized_commandset'
        trainer = bp.Models.BinaryLSTM(filemodel, filetokenizer,
                                                datasetfile, recognizeddata)
        trainer.train('command', 'evaluate')

    @classmethod
    def emotionsevaluate(cls):
        super().emotionstrain()

    @classmethod
    def hi_th_commandevaluate(cls):
        super().hi_th_commandtrain()

    @classmethod
    def multyclassevaluate(cls):
        super().multyclasstrain()

class Multyevaluate(IEvaluate):

    @classmethod
    def hievaluate(cls):
        super().hievaluate()

    @classmethod
    def quevaluate(cls):
        super().quevaluate()

    @classmethod
    def thevaluate(cls):
        super().thevaluate()

    @classmethod
    def commandevaluate(cls):
        super().commandevaluate()

    @classmethod
    def hi_th_commandevaluate(cls):
        super().hi_th_commandevaluate()

    @classmethod
    def multyclassevaluate(cls):

        trainer = bp.Models.Multy('./models/multy/LSTM/multyclassmodel.h5',
                                './tokenizers/multy/LSTM/multyclasstokenizer.pickle',
                                'SELECT * FROM multyclasesset',
                                'SELECT * FROM recognized_multyclasesset')
        trainer.train('questionclass', 3, 'evaluate', 200)

    @classmethod
    def emotionsevaluate(cls):
        trainer = bp.Models.MultyLSTM('./models/multy/LSTM/emotionsmodel.h5',
                                   './tokenizers/multy/LSTM/emotionstokenizer.pickle',
                                   'SELECT * FROM emotionstrain',
                                   'SELECT * FROM recognized_emotionstrain')
        trainer.train('emotionid', 7, 'evaluate', 200)