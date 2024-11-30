import logging
from Core_layer.Answer_package.Classes import RandomAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing


class AActionThree(IAction.IAction):
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
        AActionThree.message = message
        AActionThree.message_text = message_text

    @classmethod
    def first(cls):
#
#       агломерировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('агломерируй') > 0 and cls.message_text.count('агломерируйся') == 0:
                return cls.__ra.answer('agglomerateanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionthree.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       агломерироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('агломерируйся') > 0:
                return cls.__ra.answer('agglomerateselfanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionthree.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       агонизировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthree.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       агрегатировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthree.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       агрегатироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthree.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       агрегировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthree.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       агрегироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthree.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       агукать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('агукани') > 0:
                return 'агу'
        except Exception as e:
            logging.exception(str('The exception in aactionthree.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       агукнуть
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('агукни') > 0:
                return 'агу'
        except Exception as e:
            logging.exception(str('The exception in aactionthree.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       адаптировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthree.tenth ' + str(e)))