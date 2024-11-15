import logging
from Core_layer.Command_package.Interfaces import IAnalyzer
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Classes.CommandActions import AAction
from Core_layer.Command_package.Classes.CommandActions import BAction
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
        sc = BAction.BAction(cls.__message, message_text)
        ac = CommandAction.CommandAction(cls.__message, message_text)
        try:
            info_dict = {
                'абонировать': str(fc.first()),
                'абонироваться': str(fc.second()),
                'абсолютизировать': str(fc.third()),
                'абсолютизироваться': str(fc.fourth()),
                'абсолютировать': str(fc.fifth()),
                'абсорбировать': str(fc.sixth()),
                'абсорбироваться': str(fc.seventh()),
                'абстрагировать': str(fc.eighth()),
                'абстрагироваться': str(fc.nineth()),
                'авансировать': str(fc.tenth()),
                'авансироваться': str(fc.eleventh()),
                'авизировать': str(fc.twelth()),
                'авизироваться': str(fc.thirteenth()),
                'автоматизировать': str(fc.fourteenth()),
                'автоматизироваться': str(fc.fifteenth()),
                'авторизовать': str(fc.sixteenth()),
                'авторизоваться': str(fc.seventeenth()),
                'агглютинировать': str(fc.eithneenth()),
                'агглютинироваться': str(fc.nineteenth()),
                'агитировать': str(fc.twenttyth()),
                'агломерировать': str(fc.twentyfirst()),
                'агломерироваться': str(fc.twentysecond()),
                'агонизировать': str(fc.twentythird()),
                'агрегатировать': str(fc.twentyfourth()),
                'агрегатироваться': str(fc.twentyfifth()),
                'агрегировать': str(fc.twentysixth()),
                'агрегироваться': str(fc.twentyseventh()),
                'агукать': str(fc.twentyeighth()),
                'агукнуть': str(fc.twentynineth()),
                'адаптировать': str(fc.thirtyth()),
                'адаптироваться': str(fc.thirtyfirst()),
                'адвербиализироваться': str(fc.thirtysecond()),
                'адвокатствовать': str(fc.thirtythird()),
                'администрировать': str(fc.thirtyfourth()),
                'адоптировать': str(fc.thirtyfifth()),
                'адоптироваться': str(fc.thirtysixth()),
                'адресовать': str(fc.thirtyseventh()),
                'адресоваться': str(fc.thirtyeighth()),
                'адсорбировать': str(fc.thirynineth()),
                'адсорбироваться': str(fc.fourtyth()),
                'адъективироваться': str(fc.fourtyfirst()),
                'ажитировать': str(fc.fourtysecond()),
                'ажитироваться': str(fc.fourythird()),
                'азартничать': str(fc.fourtyfourth()),
                'азотировать': str(fc.fourtyfifth()),
                'азотироваться': str(fc.fourtysixth()),
                'айкай': str(fc.fourtyseventh()),
                'айкать': str(fc.fourtyeight()),
                'айкнуть': str(fc.fourtynineth()),
                'акать': str(fc.fiftyth()),
                'акклиматизировать': str(fc.fiftyfirst()),
                'акклиматизироваться': str(fc.fiftysecond()),
                'аккомодировать': str(fc.fiftythird()),
                'аккомодироваться': str(fc.fiftyfourth()),
                'аккомпанировать': str(fc.fiftyfifth()),
                'аккредитовать': str(fc.fiftysixth()),
                'аккредитоваться': str(fc.fiftyseventh()),
                'аккумулировать': str(fc.fiftyeight()),
                'аккумулироваться': str(fc.fiftynineth()),
                'акробатничать': str(fc.sixtyth()),
                'акробатствовать': str(fc.sixtyfirst()),
                'акселерироваться': str(fc.sixtysecond()),
                'актерствовать': str(fc.sixtythird()),
                'активизировать': str(fc.sixtyfourth()),
                'активизироваться': str(fc.sixtyfifth()),
                'активировать': str(fc.sixtysixth()),
                'активироваться': str(fc.sixsyseventh()),
                'активничать': str(fc.sixtyeighthth()),
                'актировать': str(fc.sixtynineth()),
                'актироваться': str(fc.seventyth()),
                'актуализировать': str(fc.seventyfirst()),
                'актуализироваться': str(fc.seventysecond()),
                'акушерствовать': str(fc.seventythird()),
                'акцентировать': str(fc.seventyfourth()),
                'акцентироваться': str(fc.seventyfifth()),
                'акцептовать': str(fc.seventysixth()),
                'алгоритмизировать': str(fc.seventyseventh()),
                'алгоритмизироваться': str(fc.seventyeigth()),
                'аля': str(fc.seventynineth()),
                'алеть': str(fc.eightyth()),
                'алеться': str(fc.eightyfirst()),
                'алкать': str(fc.eightysecond()),
                'алтынничать': str(fc.eightythird()),
                'амальгамировать': str(fc.eightyfourth()),
                'амальгамироваться': str(fc.eightyfifth()),
                'американизировать': str(fc.eightysixth()),
                'американизироваться': str(fc.eightyseventh()),
                'амикошонствовать': str(fc.eightyeighth()),
                'амнистировать': str(fc.eightynineth()),
                'амнистироваться': str(fc.ninetyth()),
                
                #
                'багроветь': str(sc.first()),
                'баллотировать': str(sc.second()),
                'баловать': str(sc.third()),
                'баловаться': str(sc.fourth()),
                'бальзамировать': str(sc.fifth()),
                'барабанить': str(sc.sixth()),
                'барахтаться': str(sc.seventh()),
                'баррикадировать': str(sc.eighth()),
                'барствовать': str(sc.nineth()),
                'басить': str(sc.tenth()),
                'бастовать': str(sc.eleventh()),
                'батрачить': str(sc.twelth()),
                'бегать': str(sc.thirteenth()),
                'беднеть': str(sc.fourteenth()),
                'бедокурить': str(sc.fifteenth()),
                'бедствовать': str(sc.sixteenth()),
                'бежать': str(sc.seventeenth()),
                'бездельничать': str(sc.eithneenth()),
                'беззаконничать': str(sc.nineteenth()),
                'безумствовать': str(sc.twenttyth()),
                'белеть': str(sc.twentyfirst()),
                'белить': str(sc.twentysecond()),
                'бередить': str(sc.twentythird()),
                'беречь': str(sc.twentifourth()),
                'беседовать': str(sc.twentyfifth()),
                'бесить': str(sc.twentysixth()),
                'беситься': str(sc.twentyseventh()),
                'бесноваться': str(sc.twentyeightth()),
                'беспокоиться': str(sc.twentynineth()),
                'беспутствовать': str(sc.thirty()),
                'бесславить': str(sc.thirtyfirst()),
                'бесстыдничать': str(sc.thirtysecond()),
                'бесчестить': str(sc.thirtythird()),
                'бешенствовать': str(sc.thirtyfourth()),
                'бинтовать': str(sc.thirtyfifth()),
                #
                'фас': str(ac.fas()),
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