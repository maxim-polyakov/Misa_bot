import logging
from Core_layer.Answer_package.Classes import RandomAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.API_package.Classes.Finders import WikiFinder
from Deep_layer.API_package.Classes.Finders import GoogleFinder
from Deep_layer.API_package.Classes.Calculators import SympyCalculator
from Deep_layer.API_package.Classes.Translators import MemoryTranslator
from Deep_layer.API_package.Classes.WeatherPredictors import WeatherPredictor
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing


class BActionTen(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        BActionTen.message = message
        BActionTen.message_text = message_text

    @classmethod
    def first(cls):
#
#       безуметь
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       безумствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       белый
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       белеть
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       белеться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       бель
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       белить
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       белиться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       белковать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       беллетризировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionten.tenth ' + str(e)))