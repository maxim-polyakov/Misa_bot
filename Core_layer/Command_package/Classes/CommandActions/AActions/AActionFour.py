import logging
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Core_layer.Answer_package.Classes import GptAnswer

class AActionFour(IAction.IAction):
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
        AActionFour.message = message
        AActionFour.message_text = message_text

    @classmethod
    def first(cls):
#
#       адаптироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адаптируйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       адвербиализироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адвербиализируйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       адвокатствовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адвокатствуй') > 0 and cls.message_text.count('адвокатствуйся') == 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       администрировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('администрируй') > 0 and cls.message_text.count('администрируйся') == 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       адоптировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адоптируй') > 0 and cls.message_text.count('адоптируйся') == 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       адоптироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адоптируйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       адресовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адресуй') > 0 and cls.message_text.count('адресуйся') == 0:
                message_text = (cls.message_text.strip(' ')
                                .replace('адресуй ', ''))
                if message_text.count('сообщение') > 0:
                    return 'сообщение для ' + str(cls.message.chat.username)
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       адресоваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адресуйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       адсорбировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адсорбируй') > 0 and cls.message_text.count('адсорьируйся') == 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       адсорбироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('адсорбируйся') > 0:
                return cls._gpta.answer(cls.message_text)
        except Exception as e:
            logging.exception(str('The exception in aactionfour.tenth ' + str(e)))