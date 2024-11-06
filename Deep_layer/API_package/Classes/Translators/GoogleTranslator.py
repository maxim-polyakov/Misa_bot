import pandas as pd
import logging
from googletrans import Translator
from multipledispatch import dispatch
from Deep_layer.API_package.Interfaces import ITranslator
from Deep_layer.DB_package.Classes import DB_Communication


class GoogleTranslator(ITranslator.ITranslator):
    """
    It is google translator class
    """
    _translator = Translator()

    lang = 'ru'
    def __init__(self, lang,):
        GoogleTranslator.lang = lang
    @classmethod
    def _translate(cls, inputText):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        tranlated = cls._translator.translate(inputText, dest=cls.lang)
        logging.info('The googletranslator.translate internal  is done')
        return tranlated.text
    @classmethod
    @dispatch(object, object, object)
    def translate(cls, dataselect, insertdtname):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            train = DB_Communication.DB_Communication.get_data(dataselect)
            train.text = train.text.astype(str)
            df = pd.concat([train])
            df = pd.DataFrame(df['text'])
            df['text'] = df['text'].apply(cls._translate)
            dbc = DB_Communication.DB_Communication()
            dbc.insert_to(df, 'translated')
            logging.info('The googletranslator.translate 1  is done')
            return 'Готово'
        except Exception as e:
            logging.exception(str('The exception is in googletranslator.translate ' + str(e)))
    @classmethod
    @dispatch(object, object)
    def translate(cls, inptmes):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            tranlated = cls._translate(inptmes)
            logging.info('The googletranslator.translate 2 is done')
            return tranlated
        except Exception as e:
            logging.exception(str('The exception is in googletranslatorMes.translate ' + str(e)))