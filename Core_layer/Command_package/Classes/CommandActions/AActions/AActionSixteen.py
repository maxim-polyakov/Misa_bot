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


class AActionSixteen(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        AActionSixteen.message = message
        AActionSixteen.message_text = message_text

    @classmethod
    def first(cls):
#
#       ассимилироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       ассистировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       ассоциировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       ассоциироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       асфальтировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       асфальтироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       атаковать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       атаковаться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       атаковывать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       атаковываться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.tenth ' + str(e)))