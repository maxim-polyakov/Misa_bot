import logging
from Core_layer.Command_package.Interfaces import IAnalyzer
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Classes.CommandActions import AAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing, CommonPreprocessing, CommandPreprocessing


class CommandAnalyzer(IAnalyzer.IAnalyzer):
    """
    It is command analyzer
    """
    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()
    __cpr = CommandPreprocessing.CommandPreprocessing()
    __nothingflg = 0
    __cash = ''

    def __init__(self, message, mesentype):
        CommandAnalyzer.__message = message
        CommandAnalyzer.__mesentype = mesentype

    @classmethod
    def __action_step(cls, chosen_item, message_text):
#
#
        fc = AAction.AAction(cls.__message, message_text)
        ac = CommandAction.CommandAction(cls.__message, message_text)
        try:
            info_dict = {
                'авансировать': str(fc.first()),
                'автоматизировать': str(fc.second()),
                'агитировать': str(fc.third()),
                'администрировать': str(fc.fourth()),
                'акклиматизироваться': str(fc.fifth()),
                'аккомпанировать': str(fc.sixth()),
                'активизировать': str(fc.seventh()),
                'акцентировать': str(fc.eighth()),
                'алеть': str(fc.nineth()),
                'амальгамировать': str(fc.tenth()),
                'амнистировать': str(fc.eleventh()),
                'ампутировать': str(fc.twelth()),
                'анализировать': str(fc.thirteenth()),
                'апеллировать': str(fc.fourteenth()),
                'аплодировать': str(fc.fifteenth()),
                'аргументировать': str(fc.sixteenth()),
                'арендовать': str(fc.seventeenth()),
                'арестовывать': str(fc.eithneenth()),
                'ассигновать': str(fc.nineteenth()),
                'ассистировать': str(fc.twenttyth()),
                'атаковать': str(fc.twentyfirst()),
                'аттестовывать': str(fc.twentysecond()),
                'афишировать': str(fc.twentythird()),
                'фас': str(fc.twentyfirst()),
                'перевести': str(ac.translate()),
                'поссчитать': str(ac.find()),
                'находить': str(ac.find()),
                'сказать': str(ac.say()),
                'погода': str(ac.weather()),
                'поздороваться': str(ac.sayhi()),
                'почистить': str(ac.clean()),
                'очистить': str(ac.clean())
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
                        outstr += outmes + '\n'
            logging.info('The commandanalyzer.analyse is done')
            return outstr
        except Exception as e:
            logging.exception(str('The exception in commandanalyzer.analyse ' + str(e)))