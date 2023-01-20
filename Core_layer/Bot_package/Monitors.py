from Core_layer import Bot_package


class IMonitor(Bot_package.ABC):

    @Bot_package.abstractmethod
    def monitor(self):
        pass

class MessageMonitor(IMonitor):
    _bpred = Bot_package.Predictors.BinaryLSTM()
    _nnpred = Bot_package.Predictors.NaiveBayes()
    _rfpred = Bot_package.Predictors.RandomForest()
    _mpred = Bot_package.Predictors.MultyLSTM()
    _xgpred = Bot_package.Predictors.Xgboost()

    _pr = Bot_package.TextPreprocessers.CommonPreprocessing()

    _dbc = Bot_package.DB_Bridge.DB_Communication()

    _be = Bot_package.Botoevaluaters.Binaryevaluate()
    _me = Bot_package.Botoevaluaters.Multyevaluate()
    _mapa = Bot_package.Mapas.Mapa()

    @classmethod
    def __classify_question(cls, chosen_item):
        info_dict = {
            'Дело': 'Я в порядке. ',
            'Погода': 'Погода норм. '
        }
        return info_dict.get(chosen_item, 'Вопрос без классификации. ')

    @classmethod
    def __classify(cls, chosen_item):
        ra = Bot_package.Answers.RandomAnswer()
        info_dict = {
            'Приветствие': str(ra.answer()[0]),
            'Благодарность': 'Не за что. ',
            'Дело': 'Утверждение про дела. ',
            'Погода': 'Утверждение про погоду. ',
            'Треш': 'Просьба, оставить неприличные высказывания при себе.'
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
        modelpath = next(Bot_package.Path().rglob('emotionsmodel.h5'))
        tokenizerpath = next(Bot_package.Path().rglob('emotionstokenizer.pickle'))

        emotion = cls._mpred.predict(text, cls._mapa.EMOTIONSMAPA,
                                     modelpath,
                                     tokenizerpath)
        return emotion

    @classmethod
    def _neurodesc(cls, text, text_message, command):

        modelpaths = [next(Bot_package.Path().rglob('businessmodel.h5')),
                      next(Bot_package.Path().rglob('weathermodel.h5')),
                      next(Bot_package.Path().rglob('himodel.h5')),
                      next(Bot_package.Path().rglob('thmodel.h5')),
                      next(Bot_package.Path().rglob('trashmodel.h5'))]

        tokenizerpaths = [next(Bot_package.Path().rglob('businesstokenizer.pickle')),
                          next(Bot_package.Path().rglob('weathertokenizer.pickle')),
                          next(Bot_package.Path().rglob('hitokenizer.pickle')),
                          next(Bot_package.Path().rglob('thtokenizer.pickle')),
                          next(Bot_package.Path().rglob('trashtokenizer.pickle'))]


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

        Bot_package.DB_Bridge.DB_Communication.insert_to(lowertext)
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
        MessageMonitorTelegram.__command = Bot_package.Commands.CommandAnalyzer(
            Bot_package.telegram_bot.boto, message, 'telegram')
        MessageMonitorTelegram.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command, 'telegram')

class MessageMonitorDiscord(MessageMonitor):

    def __init__(self, message):
        MessageMonitorDiscord.__command = Bot_package.Commands.CommandAnalyzer(
            Bot_package.telegram_bot.boto, message, 'discord')
        MessageMonitorDiscord.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command, 'discord')





