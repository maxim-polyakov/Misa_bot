import logging
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Core_layer.Answer_package.Classes import GptAnswer

class AActionFive(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None
    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()
    _gpta = GptAnswer.GptAnswer()

    def __init__(self, message, message_text):
        AActionFive.message = message
        AActionFive.message_text = message_text

    @classmethod
    def first(cls):
#
#       адъективироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адъективируйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       ажитировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('ажитируй') and cls.message_text.count('ажитируйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       ажитироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('ажитируйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       азартничать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('азартничай') and cls.message_text.count('азартничайся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       азотировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('азотируй') and cls.message_text.count('азотируйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       азотироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('азотируйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       айкай
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('айкай') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       айкать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('айкай') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       айкнуть
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('айкни') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       акать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('акни') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfive.tenth ' + str(e)))