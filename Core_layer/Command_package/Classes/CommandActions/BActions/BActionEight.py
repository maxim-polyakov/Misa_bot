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


class BActionEight(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        BActionEight.message = message
        BActionEight.message_text = message_text

    @classmethod
    def first(cls):
#
#       бай
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       байт
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       бдеть
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       бегать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       бедный
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       беднеть
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       бедовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       бедокурить
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       бедствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       бежать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactioneight.tenth ' + str(e)))