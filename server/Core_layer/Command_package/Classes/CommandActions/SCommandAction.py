import logging
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Core_layer.Answer_package.Classes import GptAnswer

class SCommandAction(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        SCommandAction.message = message
        SCommandAction.message_text = message_text

    @classmethod
    def first(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.first ' + str(e)))

    @classmethod
    def second(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.second ' + str(e)))

    @classmethod
    def third(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#
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
            if cls.message_text.count('атакуй') > 0  and cls.message_text.count('атакуйся') == 0:
                Inputstr = cls.__pred.preprocess_text(cls.message_text)
                Inputstr = Inputstr.replace('атакуй ', '').replace('пиздани ', '').replace('фас ', '')
                Inputarr = Inputstr.split(' ')
                cls.command_flag = 1
                Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
                logging.info('The commandaction.twentyfirst is done')
                return Inputstr + ' - пидор.'
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       атаковаться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('атакуйся') > 0:
                Inputstr = cls.__pred.preprocess_text(cls.message_text)
                Inputstr = Inputstr.replace('атакуй ', '').replace('пиздани ', '').replace('фас ', '')
                Inputarr = Inputstr.split(' ')
                cls.command_flag = 1
                Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
                logging.info('The scommandaction.eighth is done')
                return Inputstr + ' - пидор.'
        except Exception as e:
            logging.exception(str('The exception in scommandaction.eighth ' + str(e)))

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