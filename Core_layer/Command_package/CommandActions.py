from Deep_layer.NLP_package import TextPreprocessers
from Deep_layer.API_package import Calculators
from Deep_layer.API_package import Finders
from Deep_layer.API_package import Translators
from abc import ABC, abstractmethod

class IAction(ABC):

    @abstractmethod
    def fas(cls):
        pass
    @abstractmethod
    def find(cls):
        pass
    @abstractmethod
    def translate(cls):
        pass

class CommandAction(IAction):
    boto = None
    message = None
    message_text = None
    __pred = TextPreprocessers.Preprocessing()
    __pr = TextPreprocessers.CommonPreprocessing()
    def __init__(self, boto, message, message_text):
        CommandAction.message_text = message_text
        CommandAction.boto = boto
        CommandAction.message = message

    @classmethod
    def fas(cls):
        Inputstr = cls.__pred.preprocess_text(cls.message_text)
        Inputstr = Inputstr.replace('атакуй ', '').replace('пиздани ', '').replace('фас ', '')
        Inputarr = Inputstr.split(' ')
        cls.command_flag = 1
        Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
        return Inputstr + ' - пидор.'

    @classmethod
    def __calculate(cls, message_text):
        Inputarr = message_text.split(' ')
        c = Calculators.SympyCalculator()
        if cls.__pr.preprocess_text(Inputarr[0]) == 'производная':
            output = c.deravative(Inputarr[1], Inputarr[2])
            return output
        elif cls.__pr.preprocess_text(Inputarr[0]) == 'интеграл':
           output = c.integrate(Inputarr[1], Inputarr[2])
           return output
        message_text = cls.message_text.replace(Inputarr[1].rstrip(), '')
        message_text = message_text.replace(Inputarr[2], '').replace(Inputarr[0], '')
        message_text = message_text.strip(' ')
        cls.command_flag = 1
        return message_text

    @classmethod
    def find(cls):
        message_text = cls.message_text.strip(' ').replace('находить ', '').replace('поссчитать ', '')
        if (message_text.count('производная') > 0) or (message_text.count('интеграл') > 0):
            message_text = cls.__calculate(message_text)
            cls.command_flag = 1
            return message_text
        else:
            apif = Finders.WikiFinder()
            finded_list = apif.find(message_text)
            try:
                return str(finded_list)
            except:
                return "Не нашла"

    @classmethod
    def translate(cls):
        message_text = cls.message_text.strip(' ').replace('перевести ', '')
        tr = Translators.GoogleTranslator("ru")
        translated = tr.translate(message_text)
        return translated


