import logging
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Core_layer.Answer_package.Classes import GptAnswer

class AActionThirteen(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        AActionThirteen.message = message
        AActionThirteen.message_text = message_text

    @classmethod
    def first(cls):
#
#       аппретироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       апробировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       апробироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       аранжировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       аранжироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       аргументировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       аргументироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       арендовать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       арендоваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       арестовывать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionthirteen.tenth ' + str(e)))