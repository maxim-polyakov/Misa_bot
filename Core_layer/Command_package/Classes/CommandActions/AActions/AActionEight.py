import logging
from Core_layer.Answer_package.Classes import RandomAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing


class AActionEight(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        AActionEight.message = message
        AActionEight.message_text = message_text

    @classmethod
    def first(cls):
#
#       актуализировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       актуализироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       акушерствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       акцентировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       акцентироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       акцептовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       алгоритмизировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       алгоритмизироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       аля
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       алеть
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneight.tenth ' + str(e)))