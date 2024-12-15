import logging
from Core_layer.Command_package.Interfaces import IAnalyzer
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Classes.CommandActions import FCommandAction
from Core_layer.Command_package.Classes.CommandActions import SCommandAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing, CommonPreprocessing, CommandPreprocessing
from Core_layer.Answer_package.Classes import GptAnswer

class CommandAnalyzer(IAnalyzer.IAnalyzer):
    """
    It is command analyzer
    """
    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()
    __cpr = CommandPreprocessing.CommandPreprocessing()
    __nothingflg = 0
    __cash = ''
    __boto = None
    __message = None
    __mesentype = None
    _gpta = GptAnswer.GptAnswer()

    def __init__(self, boto, message, mesentype):
        CommandAnalyzer.__boto = boto
        CommandAnalyzer.__message = message
        CommandAnalyzer.__mesentype = mesentype

    @classmethod
    def __action_step(cls, chosen_item, message_text):
#
#
        try:
            aone = FCommandAction.FCommandAction(cls.__message, message_text)
            asixteen = SCommandAction.SCommandAction(cls.__message, message_text)


            ac = CommandAction.CommandAction(cls.__message, message_text)
            info_dict = {
                'абонировать': str(aone.first()),
                'абонироваться': str(aone.second()),
                'нарисовать':str(aone.third()),
                'атаковать': str(asixteen.seventh()),
                'фас': str(ac.first()),
                'перевести': str(ac.second()),
                'поссчитать': str(ac.nineth()),
                'находить': str(ac.third()),
                'сказать': str(ac.fourth()),
                'погода': str(ac.fifth()),
                'поздороваться': str(ac.sixth()),
                'почистить': str(ac.seventh()),
                'очистить': str(ac.seventh())
                }
            return info_dict[chosen_item]
        except Exception as e:
            return ''

    @classmethod
    def __action(cls, message_text):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outlist = []
            array_of_message_text = message_text.split(' ')
            for word in array_of_message_text:
                outlist.append(cls.__action_step(cls.__pr.preprocess_text(word), message_text))
            outlist = list(set(outlist))
            logging.info('The commandanalyzer.__action is done')
            return outlist
        except Exception as e:
            logging.exception(str('The exception in commandanalyzer.__action ' + str(e)))

    @classmethod
    def analyse(cls, message_text):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outstr = ''

            if (message_text.count('.') > 0):
                word_arr = message_text.split('. ')
            else:
                word_arr = message_text.split(', ')
            for word in word_arr:
                outlist = cls.__action(word)
                if (outlist != None):
                    for outmes in outlist:
                        outstr += str(outmes) + '\n'
            logging.info('The commandanalyzer.analyse is done')
            if outstr == '\n':
                return cls._gpta.answer(message_text)
            return outstr
        except Exception as e:
            logging.exception(str('The exception in commandanalyzer.analyse ' + str(e)))