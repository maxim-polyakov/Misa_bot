import logging
import requests
import os
import pandas as pd
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing

from Core_layer.Bot_package.Classes.Drawers import Drawer
from Core_layer.Answer_package.Classes import GptAnswer

class FCommandAction(IAction.IAction):
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
    __dbc = DB_Communication.DB_Communication()
    _gpta = GptAnswer.GptAnswer()

    def __init__(self, message, message_text):
        FCommandAction.message = message
        FCommandAction.message_text = message_text

    @classmethod
    def first(cls):
        # first subscribe
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
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
                return 'Добавила в базу данных' + ' '
            elif(cls.__hashone == cls.__pr.preprocess_text(text=message_text)):
                cls.__hashone == None
                return 'Уже добавляла'
        except Exception as e:
            logging.exception('The exception in aactionone.first ' + str(e))

    @classmethod
    def second(cls):
        # second subscribe
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
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
                return 'Добавила себя в базу данных' + ' '
            elif (cls.__hashtwo == cls.__pr.preprocess_text(text=message_text)):
                cls.__hashtwo == None
                return 'Уже добавляла'
        except Exception as e:
            logging.exception('The exception in aactionone.second ' + str(e))

    @classmethod
    def third(cls):
#
#       нарисуй
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            dal = Drawer.Drawer(cls.message_text)
            filepath = dal.draw()
            return filepath
        except Exception as e:
            logging.exception('The exception in aactionone.third ' + str(e))

    @classmethod
    def fourth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception('The exception in aactionone.fourth ' + str(e))

    @classmethod
    def fifth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception('The exception in aactionone.fifth ' + str(e))

    @classmethod
    def sixth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception('The exception in aactionone.sixth ' + str(e))

    @classmethod
    def seventh(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception('The exception in aactionone.seventh ' + str(e))

    @classmethod
    def eighth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception('The exception in aactionone.eighth ' + str(e))

    @classmethod
    def nineth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception('The exception in aactionone.nineth ' + str(e))

    @classmethod
    def tenth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception('The exception in aactionone.tenth ' + str(e))