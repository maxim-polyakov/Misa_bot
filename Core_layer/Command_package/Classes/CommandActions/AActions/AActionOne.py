import logging
import pandas as pd
from Core_layer.Answer_package.Classes import RandomAnswer
from Deep_layer.DB_package.Classes import DB_Communication
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.API_package.Classes.WeatherPredictors import WeatherPredictor
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing


class AActionOne(IAction.IAction):
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
    __dbc = DB_Communication.DB_Communication()

    def __init__(self, message, message_text):
        AActionOne.message = message
        AActionOne.message_text = message_text

    @classmethod
    def first(cls):
#
#       абонировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('абонируй') > 0 and cls.message_text.count('абонируйся') == 0:
                message_text = (cls.message_text.strip(' ')
                                .replace('абонируй ', ''))
                dfc = cls.__dbc.get_data('select count(subscriber) from assistant_sets.subscribetable')
                counts = dfc['count'][0]
                dbc = DB_Communication.DB_Communication()
                data = {'id': counts + 1, 'subscriber': cls.__pr.preprocess_text(text=message_text)}
                df = pd.DataFrame()
                new_row = pd.Series(data)
                df = df.append(new_row, ignore_index=True)
                if cls.__hashone == None:
                    dbc.insert_to(df, 'subscribetable', 'assistant_sets')
                    cls.__hashone = cls.__pr.preprocess_text(text=message_text)
                    return cls.__ra.answer('subscribeanswer') + ' '
                elif(cls.__hashone == cls.__pr.preprocess_text(text=message_text)):
                    cls.__hashone == None
                    return 'Уже добавляла'
        except Exception as e:
            logging.exception(str('The exception in aactionone.first ' + str(e)))

    @classmethod
    def second(cls):
#
#       абонироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('абонируйся') > 0:
                message_text = 'миса'
                dfc = cls.__dbc.get_data('select count(subscriber) from assistant_sets.subscribetable')
                counts = dfc['count'][0]
                dbc = DB_Communication.DB_Communication()
                data = {'id': counts + 1, 'subscriber': message_text}
                df = pd.DataFrame()
                new_row = pd.Series(data)
                df = df.append(new_row, ignore_index=True)
                if cls.__hashtwo == None:
                    dbc.insert_to(df, 'subscribetable', 'assistant_sets')
                    cls.__hashtwo = cls.__pr.preprocess_text(text=message_text)
                    return cls.__ra.answer('subscribeself') + ' '
                elif (cls.__hashtwo == cls.__pr.preprocess_text(text=message_text)):
                    cls.__hashtwo == None
                    return 'Уже добавляла'
        except Exception as e:
            logging.exception(str('The exception in aactionone.second ' + str(e)))

    @classmethod
    def third(cls):
#
#       абсолютизировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('абсолютизируй') > 0 and cls.message_text.count('абсолютизируйся') == 0:
                return cls.__ra.answer('absolutizeanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionone.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#       абсолютизироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('абсолютизируйся') > 0:
                return cls.__ra.answer('absolutizeselfanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionone.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#       абсолютировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('абсолютируй') > 0 and cls.message_text.count('абсолютируйся') == 0:
                return cls.__ra.answer('to_absolutizeanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionone.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#       абсорбировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('абсорбируй') > 0 and cls.message_text.count('абсорбируйся') == 0:
                return cls.__ra.answer('absorbanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionone.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       абсорбироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('абсорбируйся') > 0:
                return cls.__ra.answer('absorbselfanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionone.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       абстрагировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('абстрагируй') > 0 and cls.message_text.count('абстрагируйся') == 0:
                return cls.__ra.answer('abstractanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionone.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       абстрагироваться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('абстрагируйся') > 0:
                return cls.__ra.answer('abstractselfanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionone.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       авансировать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('авансируй') > 0 and cls.message_text.count('авансируйся') == 0:
                return cls.__ra.answer('advanceanswer')
        except Exception as e:
            logging.exception(str('The exception in aactionone.tenth ' + str(e)))