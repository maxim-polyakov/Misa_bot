import logging
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Core_layer.Answer_package.Classes import GptAnswer

class AActionEleven(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        AActionEleven.message = message
        AActionEleven.message_text = message_text

    @classmethod
    def first(cls):
#
#       англизироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       анестезировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       анкетировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       аннексировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       аннексироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       аннигилироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       аннотировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       аннотироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       аннулировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       аннулироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactioneleven.tenth ' + str(e)))