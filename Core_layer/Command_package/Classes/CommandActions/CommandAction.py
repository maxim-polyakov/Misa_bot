import logging
from Core_layer.Answer_package.Classes import RandomAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.API_package.Classes.Finders import WikiFinder
from Deep_layer.API_package.Classes.Finders import GoogleFinder
from Deep_layer.API_package.Classes.Calculators import SympyCalculator
from Deep_layer.API_package.Classes.Translators import GoogleTranslator
from Deep_layer.API_package.Classes.WeatherPredictors import WeatherPredictor
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
    def fas(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            Inputstr = cls.__pred.preprocess_text(cls.message_text)
            Inputstr = Inputstr.replace('атакуй ', '').replace('пиздани ', '').replace('фас ', '')
            Inputarr = Inputstr.split(' ')
            cls.command_flag = 1
            Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
            logging.info('The commandaction.fas is done')
            return Inputstr + ' - пидор.'
        except Exception as e:
            logging.exception(str('The exception in commandaction.fas ' + str(e)))

    @classmethod
    def calculate(cls,):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            message_text = (cls.message_text.strip(' ')
                            .replace('найди ', '')
                            .replace('поссчитай ', ''))
            Inputarr = message_text.split(' ')
            c = SympyCalculator.SympyCalculator()
            if Inputarr[0] == 'производную':
                output = c.deravative(Inputarr[1], Inputarr[3])
                logging.info('The commandaction.calculate is done')
                return output
            elif Inputarr[0] == 'интеграл':
                output = c.integrate(Inputarr[1], Inputarr[3])
                logging.info('The commandaction.calculate is done')
                return output
            else:
                outputone = c.deravative(Inputarr[1], Inputarr[3])
                outputtwo = c.integrate(Inputarr[1], Inputarr[3])
                output = 'производная ' + outputone + ', ' +'интеграл '+ outputtwo
                logging.info('The commandaction.calculate is done')
                return output
            message_text = cls.message_text.replace(Inputarr[1].rstrip(), '')
            message_text = message_text.replace(Inputarr[2], '').replace(Inputarr[0], '')
            message_text = message_text.strip(' ')
            cls.command_flag = 1
            logging.info('The commandaction.calculate is done')
            return message_text
        except Exception as e:
            logging.exception(str('The exception in commandaction.calculate ' + str(e)))

    @classmethod
    def find(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        message_text = (cls.message_text.strip(' ')
                        .replace('найди ', '')
                        .replace('поссчитай ', ''))
        if (message_text.count('производную') > 0) or (message_text.count('интеграл') > 0):
            message_text = cls.calculate()
            cls.command_flag = 1
            logging.info('The commandaction.find is done')
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
                    logging.exception(str('The exception in commandaction.find ' + str(e)))
                    return "Не нашла"
            else:
                try:
                    gpif = GoogleFinder.GoogleFinder()
                    finded_list = gpif.find(message_text)
                    outstr = ''
                    if (finded_list != None):
                        for outmes in finded_list:
                            outstr += outmes + ' \n '
                    logging.info('The commandaction.find is done')
                    return outstr
                except Exception as e:
                    logging.exception(str('The exception in commandaction.find ' + str(e)))
                    return "Не нашла"

    @classmethod
    def translate(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            message_text = cls.message_text.strip(' ').replace('перевести ', '')
            tr = GoogleTranslator.GoogleTranslator("ru")
            translated = tr.translate(message_text)
            logging.info('The commandaction.translate is done')
            return translated
        except Exception as e:
            logging.exception(str('The exception in commandaction.translate ' + str(e)))
            return 'Проблемы с сервисом'

    @classmethod
    def weather(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            message = cls.message_text.replace('погода ','')
            wp = WeatherPredictor.WetherPredictor(message)
            res = wp.predict()
            if res != None:
                out = str(res[0] + '. ' + res[1])
                logging.info('The commandaction.weather is done')
                return out
            logging.info('The commandaction.weather is done')
        except Exception as e:
            logging.exception(str('The exception in commandaction.weather ' + str(e)))
            return 'Проблемы с сервисом'

    @classmethod
    def say(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            message_text = cls.message_text.replace('скажи ', '')
            return message_text
        except Exception as e:
            logging.exception(str('The exception in commandaction.say ' + str(e)))

    @classmethod
    def sayhi(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            ra = RandomAnswer.RandomAnswer()
            return str(ra.answer('hianswer')) + ' '
        except Exception as e:
            logging.exception(str('The exception in commandaction.say ' + str(e)))


    @classmethod
    def clean(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            message_text = (cls.message_text.replace('почисти ', '')
                                            .replace('очисти', ''))
            pr = CommonPreprocessing.CommonPreprocessing()
            return pr.preprocess_text(message_text)
        except Exception as e:
            logging.exception(str('The exception in commandaction.say ' + str(e)))