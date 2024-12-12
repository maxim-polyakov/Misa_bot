import logging
from Core_layer.Answer_package.Classes import RandomAnswer
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Core_layer.Answer_package.Classes import GptAnswer

class AActionTwelve(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None
    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()
    __ra = RandomAnswer.RandomAnswer()

    def __init__(self, message, message_text):
        AActionTwelve.message = message
        AActionTwelve.message_text = message_text

    @classmethod
    def first(cls):
#
#       анодировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       анодироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       анонсировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       анонсироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       антидатировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       антидатироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       антрепренерствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       апеллировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       аплодировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('аплодируй') > 0 and cls.message_text.count('аплодируйся') == 0:
                return cls.__ra.answer('applaudanswer')
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       аппретировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactiontwelve.tenth ' + str(e)))