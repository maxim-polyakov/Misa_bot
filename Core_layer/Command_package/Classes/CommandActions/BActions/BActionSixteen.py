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


class BActionSixteen(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        BActionSixteen.message = message
        BActionSixteen.message_text = message_text

    @classmethod
    def first(cls):
#
#       благословляться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       благотворительствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       благотворить
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       благоустраивать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       благоустраиваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       благоухать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       блаженствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       блажь
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       блажить
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       бланшировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in bactionsixteen.tenth ' + str(e)))