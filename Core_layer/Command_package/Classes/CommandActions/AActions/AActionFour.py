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


class AActionFour(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        AActionFour.message = message
        AActionFour.message_text = message_text

    @classmethod
    def first(cls):
#
#       адаптироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адаптируйся') > 0:
                return 'Адаптируюсь'
        except Exception as e:
            logging.exception(str('The exception in aactionfour.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       адвербиализироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адвербиализируйся') > 0:
                return 'Адвербиализируюсь'
        except Exception as e:
            logging.exception(str('The exception in aactionfour.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       адвокатствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адвокатствуй') > 0 and cls.message_text.count('адвокатствуйся') == 0:
                return 'Адвокатствую'
        except Exception as e:
            logging.exception(str('The exception in aactionfour.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       администрировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('администрируй') > 0 and cls.message_text.count('администрируйся') == 0:
                return 'Я администрирую собственную память'
        except Exception as e:
            logging.exception(str('The exception in aactionfour.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       адоптировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адоптируй') > 0 and cls.message_text.count('адоптируйся') == 0:
                return 'Адоптирую'
        except Exception as e:
            logging.exception(str('The exception in aactionfour.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       адоптироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адоптируйся') > 0:
                return 'Адоптируюсь'
        except Exception as e:
            logging.exception(str('The exception in aactionfour.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       адресовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionfour.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       адресоваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionfour.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       адсорбировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionfour.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       адсорбироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionfour.tenth ' + str(e)))