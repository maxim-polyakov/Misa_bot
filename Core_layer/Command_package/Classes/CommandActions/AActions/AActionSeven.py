import logging
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Core_layer.Answer_package.Classes import GptAnswer

class AActionSeven(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        AActionSeven.message = message
        AActionSeven.message_text = message_text

    @classmethod
    def first(cls):
#
#       акробатствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       акселерироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       актерствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       активизировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       активизироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       активировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       активироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       активничать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       актировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       актироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionseven.tenth ' + str(e)))