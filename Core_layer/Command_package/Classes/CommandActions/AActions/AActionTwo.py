import logging
from Core_layer.Answer_package.Classes import RandomAnswer
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.DB_package.Classes import DB_Communication
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing


class AActionTwo(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None
    __hashone = None
    __hashtwo = None
    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()
    __ra = RandomAnswer.RandomAnswer()

    def __init__(self, message, message_text):
        AActionTwo.message = message
        AActionTwo.message_text = message_text

    @classmethod
    def first(cls):
#
#       авансироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('авансируйся') > 0:
                return cls.__ra.answer('advanceselfanswer')
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       авизировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('авизируй') > 0 and cls.message_text.count('авизируйся') == 0:
                return cls.__ra.answer('adviseanswer')
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       авизироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('авизируйся') > 0:
                return cls.__ra.answer('adviseselfanswer')
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       автоматизировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('автоматизируй') > 0 and cls.message_text.count('автоматизируйся') == 0:
                return cls.__ra.answer('automateanswer')
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       автоматизироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('автоматизируйся') > 0:
                return cls.__ra.answer('automateselfanswer')
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       авторизовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('авторизуй') > 0 and cls.message_text.count('авторизуйся') == 0:
                return 'Авторизовала'
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       авторизоваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('авторизуйся') > 0:
               return 'Авторизовалась'
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       агглютинировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('агглютинируй') > 0 and cls.message_text.count('агглютинируйся') == 0:
                return 'Аглютинирую'
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       агглютинироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('агглютинируйся') > 0:
                return 'Аглютинируюсь'
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       агитировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('агитируй') > 0 and cls.message_text.count('агитируйся') == 0:
                return cls.__ra.answer('agitateanswer')
        except Exception as e:
            logging.exception(str('The exception in aactiontwo.tenth ' + str(e)))