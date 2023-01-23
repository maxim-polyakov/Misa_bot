from pathlib import Path
from Deep_layer.NLP_package import Predictors
from Core_layer.Answer_package import Answers
from Deep_layer.NLP_package import Mapas
from Deep_layer.NLP_package import TextPreprocessers
import Front_layer.telegram_bot as telegram_bot
from Core_layer.Command_package import Commands
from abc import ABC, abstractmethod
from Deep_layer.DB_package import DB_Bridge

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

    @classmethod
    def __classify_question(cls, chosen_item):
        info_dict = {
            'Дело': 'Я в порядке. ',
            'Погода': 'Погода норм. '
        }
        return info_dict.get(chosen_item, 'Вопрос без классификации. ')

    @classmethod
    def __classify(cls, chosen_item):
        ra = Answers.RandomAnswer()
        info_dict = {
            'Приветствие': str(ra.answer()[0]),
            'Благодарность': 'Не за что. ',
            'Дело': 'Утверждение про дела. ',
            'Погода': 'Утверждение про погоду. ',
            'Треш': 'Просьба, оставить неприличные высказывания при себе. '
        }
        return info_dict.get(chosen_item, 'Нет классификации. ')

    @classmethod
    def __decision(cls, text_message, emotion, b_predictor, w_predictor, hi_predictor, th_predictor, tr_predictor, commands):
        if (cls._dbc.checkcommands(text_message)):
            return commands.commandanalyse(text_message)
        elif (text_message.count('?') > 0):
            outlist = []
            outlist.append(cls.__classify_question(w_predictor))
            outlist.append(cls.__classify_question(b_predictor))
            outlist = list(set(outlist))
            outlistuncleaned = ['Вопрос без классификации. ']
            try:
                outlist.remove('Вопрос без классификации. ')
            except:
                return ['Exception', ' ' + emotion]
            outlistcleaned = outlist
            if (len(outlistcleaned) == 0):
                outlistuncleaned.append(' ' + emotion)
                return outlistuncleaned
            else:
                outlistcleaned.append(' ' + emotion)
                return outlistcleaned
        else:
            outlist = []
            outlist.append(cls.__classify(w_predictor))
            outlist.append(cls.__classify(b_predictor))
            outlist.append(cls.__classify(hi_predictor))
            outlist.append(cls.__classify(th_predictor))
            outlist.append(cls.__classify(tr_predictor))
            outlist = list(set(outlist))
            outlistuncleaned = ['Нет классификации. ']
            try:
                outlist.remove('Нет классификации. ')
            except:
                return ['Exception', ' ' + emotion]
            outlistcleaned = outlist

            if (len(outlistcleaned) == 0):
                outlistuncleaned.append(' ' + emotion)
                return outlistuncleaned
            else:
                outlistcleaned.append(' ' + emotion)
                return outlistcleaned

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

        modelpaths = [next(Path().rglob('businessmodel.h5')),
                      next(Path().rglob('weathermodel.h5')),
                      next(Path().rglob('himodel.h5')),
                      next(Path().rglob('thmodel.h5')),
                      next(Path().rglob('trashmodel.h5'))]

        tokenizerpaths = [next(Path().rglob('businesstokenizer.pickle')),
                          next(Path().rglob('weathertokenizer.pickle')),
                          next(Path().rglob('hitokenizer.pickle')),
                          next(Path().rglob('thtokenizer.pickle')),
                          next(Path().rglob('trashtokenizer.pickle'))]


        emotion = cls._emotionsrecognition(text)

        b_predictor = cls._bpred.predict(text, cls._mapa.BUSINESSMAPA,
                                         modelpaths[0],
                                         tokenizerpaths[0],
                                         '')
        w_predictor = cls._bpred.predict(text, cls._mapa.WEATHERMAPA,
                                         modelpaths[1],
                                         tokenizerpaths[1],
                                         '')

        hi_predictor = cls._bpred.predict(text, cls._mapa.HIMAPA,
                                          modelpaths[2],
                                          tokenizerpaths[2],
                                          '')
        th_predictor = cls._bpred.predict(text, cls._mapa.THMAPA,
                                          modelpaths[3],
                                          tokenizerpaths[3],
                                          '')
        tr_predicotr = cls._bpred.predict(text, cls._mapa.TRMAPA,
                                          modelpaths[4],
                                          tokenizerpaths[4],
                                          '')

        return cls.__decision(text_message,
                              emotion,
                              b_predictor,
                              w_predictor,
                              hi_predictor,
                              th_predictor,
                              tr_predicotr,
                              command)

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





