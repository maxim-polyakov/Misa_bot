from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Deep_layer.API_package.Classes.Calculators import SympyCalculator
from Deep_layer.API_package.Classes.Finders import WikiFinder
from Deep_layer.API_package.Classes.Finders import BingFinder
from Deep_layer.API_package.Classes.Translators import GoogleTranslator
from Deep_layer.API_package.Classes.WeatherPredictors import WeatherPredictor
from Core_layer.Command_package.Interfaces import IAction

class CommandAction(IAction.IAction):
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


        Inputstr = cls.__pred.preprocess_text(cls.message_text)
        Inputstr = Inputstr.replace('атакуй ', '').replace('пиздани ', '').replace('фас ', '')
        Inputarr = Inputstr.split(' ')
        cls.command_flag = 1
        Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
        return Inputstr + ' - пидор.'

    @classmethod
    def calculate(cls,):


        message_text = (cls.message_text.strip(' ')
                        .replace('найди ', '')
                        .replace('поссчитай ', ''))
        Inputarr = message_text.split(' ')
        c = SympyCalculator.SympyCalculator()
        if Inputarr[0] == 'производную':
            output = c.deravative(Inputarr[1], Inputarr[3])
            return output
        elif Inputarr[0] == 'интеграл':
            output = c.integrate(Inputarr[1], Inputarr[3])
            return output
        else:
            outputone = c.deravative(Inputarr[1], Inputarr[3])
            outputtwo = c.integrate(Inputarr[1], Inputarr[3])
            output = 'производная ' + outputone + ', ' +'интеграл '+ outputtwo
            return output
        message_text = cls.message_text.replace(Inputarr[1].rstrip(), '')
        message_text = message_text.replace(Inputarr[2], '').replace(Inputarr[0], '')
        message_text = message_text.strip(' ')
        cls.command_flag = 1
        return message_text


    @classmethod
    def find(cls):


        message_text = (cls.message_text.strip(' ')
                        .replace('найди ', '')
                        .replace('поссчитай ', ''))
        if (message_text.count('производную') > 0) or (message_text.count('интеграл') > 0):
            message_text = cls.calculate()
            cls.command_flag = 1
            return message_text
        else:
            if (message_text.count('википедии') > 0):
                message_text = (message_text.strip(' ')
                                .replace('википедии ', ''))
                try:
                    apif = WikiFinder.WikiFinder()
                    finded_list = apif.find(cls.__pr.preprocess_text(message_text))
                    return str(finded_list)
                except:
                    return "Не нашла"
            else:
                try:
                    bpif = BingFinder.BingFinder()
                    finded_list = bpif.find(message_text)
                    outstr = ''
                    if (finded_list != None):
                        for outmes in finded_list:
                            outstr += outmes + ' '
                    return outstr
                except Exception as e:
                    return "Не нашла"


    @classmethod
    def translate(cls):


        try:
            message_text = cls.message_text.strip(' ').replace('перевести ', '')
            tr = GoogleTranslator.GoogleTranslator("ru")
            translated = tr.translate(message_text)
            return translated
        except Exception as e:
            return 'Проблемы с сервисом'
    @classmethod
    def weather(cls):


        try:
            message = cls.message_text.replace('погода ','')
            wp = WeatherPredictor.WetherPredictor(message)
            res = wp.predict()
            out = str(res[0] + '. ' + res[1])
            return out
        except Exception as e:
            return 'Проблемы с сервисом'
