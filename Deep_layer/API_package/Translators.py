from googletrans import Translator
import pandas as pd
from Deep_layer.DB_package import DB_Bridge
from multipledispatch import dispatch
from abc import ABC, abstractmethod

class ITranslator(ABC):

    @abstractmethod
    def translate(self):
        pass

class GoogleTranslator(ITranslator):


    _translator = Translator()

    lang = 'ru'
    def __init__(self, lang,):
        GoogleTranslator.lang = lang

    @classmethod
    def _translate(cls, inputText):
        tranlated = cls._translator.translate(inputText, dest=cls.lang)
        return tranlated.text

    @classmethod
    @dispatch(object, object, object)
    def translate(cls, dataselect, insertdtname):
        try:
            train = DB_Bridge.DB_Communication.get_data(dataselect)
            train.text = train.text.astype(str)

            df = pd.concat([train])
            df = pd.DataFrame(df['text'])
            df['text'] = df['text'].apply(cls._translate)

            DB_Bridge.DB_Communication.insert_to(df, 'translated')

            return 'Готово'
        except:
            print('The exception is in GoogleTranslator.translate')

    @classmethod
    @dispatch(object, object)
    def translate(cls, inptmes):
        try:
            tranlated = cls._translate(inptmes)

            return tranlated
        except:
            print('The exception is in GoogleTranslatorMes.translate')