from pathlib import Path
from Deep_layer.NLP_package import Predictors
from Core_layer.Answer_package import Answers
from Deep_layer.NLP_package import Mapas
from Deep_layer.NLP_package import TextPreprocessers
import Front_layer.telegram_bot as telegram_bot
from Core_layer.Command_package import Commands
from abc import ABC, abstractmethod
from Deep_layer.DB_package import DB_Bridge
import os

class IMonitor(ABC):

    @abstractmethod
    def monitor(self):
        pass

class MessageMonitor(IMonitor):

    _bpred = Predictors.BinaryLSTM()
    _nnpred = Predictors.NaiveBayes()
    _rfpred = Predictors.RandomForest()
    _mpred = Predictors.MultyLSTM()
    _xgpred = Predictors.Xgboost()
    _pr = TextPreprocessers.CommonPreprocessing()
    _dbc = DB_Bridge.DB_Communication()
    _mapa = Mapas.Mapa()
    _mapaslist = Mapas.ListMapas()
    qa = Answers.QuestionAnswer()
    __text_message = None
    @classmethod
    def __classify_question(cls, chosen_item):
        try:
            ra = Answers.RandomAnswer()

            info_dict = {
                'Приветствие': str(ra.answer()[0]) + ' ',
                'Благодарность': 'не за что. ',
                'Дело': cls.qa.answer(cls.__text_message),
                'Погода': cls.qa.answer(cls.__text_message),
                'Треш': 'просьба, оставить неприличные высказывания при себе. '
                }
            return info_dict[chosen_item]
        except:
            return ''

    @classmethod
    def __classify(cls, chosen_item):
        try:
            ra = Answers.RandomAnswer()
            info_dict = {
                'Приветствие': str(ra.answer()[0]) + ' ',
                'Благодарность': 'не за что. ',
                'Дело': 'утверждение про дела. ',
                'Погода': 'утверждение про погоду. ',
                'Треш': 'просьба, оставить неприличные высказывания при себе. '
            }
            return info_dict[chosen_item]
        except:
            return ''

    @classmethod
    def __decision(cls, text_message, emotion, commands,predicts):
        if (cls._dbc.checkcommands(text_message)):
            return commands.commandanalyse(text_message)
        elif (text_message.count('?') > 0):
            outlist = []

            qu = cls.qa.answer(text_message)
            outlist.append(qu.title())
        else:
            outlist = []

            for predict in predicts:
                outlist.append(cls.__classify(predict))

        outlist.append(' ' + emotion)
        return outlist

    @classmethod
    def _emotionsrecognition(cls, text):
        modelpath = next(Path().rglob('emotionsmodel.h5'))
        tokenizerpath = next(Path().rglob('emotionstokenizer.pickle'))

        emotion = cls._mpred.predict(text, cls._mapa.EMOTIONSMAPA,
                                     modelpath,
                                     tokenizerpath)
        return emotion

    @classmethod
    def _neurodesc(cls, text, text_message, command):
        cls.__text_message = text_message
        fullPathModels = str(next(Path().rglob('models')))
        fullPathTokenizers = str(next(Path().rglob('tokenizers')))
        modelarr = os.listdir(fullPathModels + '/binary/LSTM/')

        tokenizerarr = os.listdir(fullPathTokenizers + '/binary/LSTM/')
        modelpaths = []
        tokenizerpaths = []
        for model in modelarr:
            modelpaths.append(str(fullPathModels) + '/binary/LSTM/' + str(model))

        for tokenizer in tokenizerarr:
            tokenizerpaths.append(str(fullPathTokenizers) + '/binary/LSTM/' + str(tokenizer))

        emotion = cls._emotionsrecognition(text)

        predicts = []
        mapaslist = cls._mapaslist.getlistmapas()
        for id in range(0, len(modelpaths)):
            predicts.append(cls._bpred.predict(text, mapaslist[id],
                                         modelpaths[id],
                                         tokenizerpaths[id], ''))

        return cls.__decision(text_message,
                              emotion,
                              command,
                              predicts)

    @classmethod
    def monitor(cls, message, command, pltype):
        text = []

        if(pltype == 'discord'):
            lowertext = message.content.lower()
        else:
            lowertext = message.text.lower()

            DB_Bridge.DB_Communication.insert_to(lowertext)

        outstr = ''

        if (lowertext.count('миса') > 0 or lowertext.lower().count('misa') > 0):
            lowertext = lowertext.replace('миса ', '').replace('misa ', '')
            text.append(lowertext)
            outlist = cls._neurodesc(text, lowertext, command)
            if (outlist != None):
                for outmes in outlist:
                    outstr += outmes
            return outstr
        else:
            return outstr

class MessageMonitorTelegram(MessageMonitor):

    def __init__(self, message):
        MessageMonitorTelegram.__command = Commands.CommandAnalyzer(
            telegram_bot.boto, message, 'telegram')
        MessageMonitorTelegram.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command, 'telegram')

class MessageMonitorDiscord(MessageMonitor):

    def __init__(self, message):
        MessageMonitorDiscord.__command = Commands.CommandAnalyzer(
            telegram_bot.boto, message, 'discord')
        MessageMonitorDiscord.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command, 'discord')





