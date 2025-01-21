import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Bot_package.Classes.Weather import Weather
from Core_layer.Bot_package.Classes.Finder import GoogleFinder
from Core_layer.Bot_package.Classes.Finder import WikiFinder
from Core_layer.Bot_package.Classes.Translator import MemoryTranslator
from Core_layer.Command_package.Interfaces import IAction
#from Deep_layer.API_package.Classes.Finders import WikiFinder
#from Deep_layer.API_package.Classes.Finders import GoogleFinder
from Deep_layer.API_package.Classes.Calculators import SympyCalculator
#from Deep_layer.API_package.Classes.Translators import MemoryTranslator
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing


class CommandAction(IAction.IAction):
    """
    It is class for comand's actions
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        CommandAction.message = message
        CommandAction.message_text = message_text

    @classmethod
    def first(cls):
#
#       фас
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('фас') > 0:
                Inputstr = cls.__pred.preprocess_text(cls.message_text)
                Inputstr = Inputstr.replace('атакуй ', '').replace('пиздани ', '').replace('фас ', '')
                Inputarr = Inputstr.split(' ')
                cls.command_flag = 1
                Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
                logging.info('The commandaction.twentyfirst is done')
                return Inputstr + ' - пидор.'
        except Exception as e:
            logging.exception(str('The exception in aaction.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       перевести
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('переведи') > 0:
                message_text = (cls.message_text.strip(' ')
                                .replace('переведи ', ''))
                tr = MemoryTranslator.MemoryTranslator('russian')
                translated = tr.translate(message_text)
                logging.info('The commandaction.translate is done')
                return translated
            pass
        except Exception as e:
            logging.exception(str('The exception in commandaction.second ' + str(e)))
            return 'Проблемы с сервисом'

    @classmethod
    def third(cls):
#
#       находить
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('найди') > 0 and cls.message_text.count('найдись') == 0:
                message_text = (cls.message_text.strip(' ')
                                .replace('найди ', ''))
                if (message_text.count('производную') > 0) or (message_text.count('интеграл') > 0):
                    message_text = cls.__calculate()
                    cls.command_flag = 1
                    logging.info('The commandaction.third is done')
                    return message_text
                else:
                    if (message_text.count('википедии') > 0):
                        message_text = (message_text.strip(' ')
                                        .replace('википедии ', ''))
                        try:
                            apif = WikiFinder.WikiFinder()
                            finded_list = apif.find(cls.__pr.preprocess_text(message_text))
                            logging.info('The commandaction.find is done')
                            return str(finded_list)
                        except Exception as e:
                            logging.exception(str('The exception in commandaction.third ' + str(e)))
                            return 'Не нашла'
                    else:
                        try:

                            gpif = GoogleFinder.GoogleFinder(message_text)
                            outstr = gpif.find()
                            logging.info('The commandaction.find is done')
                            return outstr
                        except Exception as e:
                            logging.exception(str('The exception in commandaction.third ' + str(e)))
                            return 'Не нашла'
        except Exception as e:
            logging.exception(str('The exception in commandaction.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       сказать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('скажи') > 0:
                message_text = cls.message_text.replace('скажи ', '')
                return message_text
        except Exception as e:
            logging.exception(str('The exception in commandaction.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       погода
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('погода') > 0:
                message = cls.message_text.replace('погода ','')
                w = Weather.Weather(message)
                out = w.predict()
                return out
                logging.info('The commandaction.fifth is done')
        except Exception as e:
            logging.exception(str('The exception in commandaction.fifth ' + str(e)))
            return 'Проблемы с сервисом'

    @classmethod
    def sixth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in commandaction.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       почистить
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('почисти') > 0 and cls.message_text.count('почистись') == 0:
                message_text = (cls.message_text.replace('почисти ', ''))
                pr = CommonPreprocessing.CommonPreprocessing()
                return pr.preprocess_text(message_text)
        except Exception as e:
            logging.exception(str('The exception in commandaction.seventh ' + str(e)))

    @classmethod
    def __calculate(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:

            message_text = (cls.message_text.strip(' ')
                            .replace('поссчитай ', ''))
            Inputarr = message_text.split(' ')
            c = SympyCalculator.SympyCalculator()
            if Inputarr[0] == 'производную':
                output = c.deravative(Inputarr[1], Inputarr[3])
                logging.info('The commandaction.eighth is done')
                return output
            elif Inputarr[0] == 'интеграл':
                output = c.integrate(Inputarr[1], Inputarr[3])
                logging.info('The commandaction.eighth is done')
                return output
            else:
                outputone = c.deravative(Inputarr[1], Inputarr[3])
                outputtwo = c.integrate(Inputarr[1], Inputarr[3])
                output = 'производная ' + outputone + ', ' + 'интеграл ' + outputtwo
                logging.info('The commandaction.eighth is done')
                return output
            message_text = cls.message_text.replace(Inputarr[1].rstrip(), '')
            message_text = message_text.replace(Inputarr[2], '').replace(Inputarr[0], '')
            message_text = message_text.strip(' ')
            cls.command_flag = 1
            logging.info('The commandaction.eighth is done')
            return message_text
        except Exception as e:
            logging.exception(str('The exception in commandaction.eighth ' + str(e)))

    @classmethod
    def eighth(cls):
        pass

    @classmethod
    def nineth(cls):
#
#       поссчитай
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('поссчитай') > 0 and cls.message_text.count('поссчитайся') == 0:
                message_text = (cls.message_text.strip(' ')
                            .replace('поссчитай ', ''))
                if (message_text.count('производную') > 0) or (message_text.count('интеграл') > 0):
                    message_text = cls.__calculate()
                    cls.command_flag = 1
                    logging.info('The commandaction.nineth is done')
                    return message_text
        except Exception as e:
            logging.exception(str('The exception in commandaction.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       очистить
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('очисти') > 0 and cls.message_text.count('очисться') == 0:
                message_text = (cls.message_text.replace('почисти ', '')
                                .replace('очисти', ''))
                pr = CommonPreprocessing.CommonPreprocessing()
                return pr.preprocess_text(message_text)
        except Exception as e:
            logging.exception(str('The exception in commandaction.seventh ' + str(e)))
