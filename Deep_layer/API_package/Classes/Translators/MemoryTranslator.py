import pandas as pd
import logging
from deep_translator import MyMemoryTranslator
from multipledispatch import dispatch
from Deep_layer.API_package.Interfaces import ITranslator
from Deep_layer.DB_package.Classes import DB_Communication


class MemoryTranslator(ITranslator.ITranslator):
    """
    It is deep_translator translator class
    """
    #_translator = Translator()

    lang = 'russian'
    def __init__(self, lang,):
        MyMemoryTranslator.lang = lang
    @classmethod
    def _translate(cls, inputText):
#
#       Its method for translate sentenses
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        translator = MyMemoryTranslator(source='english', target=cls.lang)
        translated = translator.translate(text=inputText)
        #tranlated = cls._translator.translate(inputText, dest=cls.lang)
        logging.info('The mymemorytranslator.translate internal  is done')
        return translated
    @classmethod
    @dispatch(object, object, object)
    def translate(cls, dataselect, insertdtname):
#
#       its method for translating the tables
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
#       Its a base method for translating the sentences
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            tranlated = cls._translate(inptmes)
            logging.info('The googletranslator.translate 2 is done')
            return tranlated
        except Exception as e:
            logging.exception(str('The exception is in googletranslatorMes.translate ' + str(e)))