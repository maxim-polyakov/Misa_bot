from Deep_layer.NLP_package import TextPreprocessers
from abc import ABC, abstractmethod
from Deep_layer.DB_package import DB_Bridge
import pandas as pd


class ICleaner(ABC):

    @abstractmethod
    def clean(cls):
        pass

class MisaMemoryCleater(ICleaner):
    __pr = TextPreprocessers.CommonPreprocessing()
    dbname = None

    def __init__(self, dbname):
        MisaMemoryCleater.dbname = dbname

    @classmethod
    def clean(cls):
        df = DB_Bridge.DB_Communication.get_data(
            'SELECT * from train_sets.' + cls.dbname)
        df['text'] = df['text'].apply(cls.__pr.preprocess_text)

        DB_Bridge.DB_Communication.delete_data('DELETE FROM train_sets.' + cls.dbname)

        DB_Bridge.DB_Communication.insert_to(df, cls.dbname, 'train_sets')

class CommonCleaner(ICleaner):
    __pr = TextPreprocessers.CommonPreprocessing()
    _type_doc = 'xlsx'

    def __init__(self, type_doc):
        CommonCleaner._type_doc = type_doc

    @classmethod
    def clean(cls, filename, string):
        if(cls._type_doc == 'csv'):
            train = pd.read_csv(filename, encoding='utf-8')
        else:
            train = pd.read_excel(filename)
        train.text = train.text.astype(str)
        df = pd.concat([train])
        df['text'] = df['text'].apply(cls.__pr.preprocess_text)
        train = df[~df[string].isna()]
        train[string] = train[string].astype(int)
        if (cls._type_doc == 'csv'):
            train.to_csv(filename, index=False)
        else:
            train.to_excel(filename, index=False)

class QuestionCleaner(ICleaner):
    __pr = TextPreprocessers.QuestionPreprocessing()
    _type_doc = "xlsx"
    def __init__(self, type_doc):
        QuestionCleaner._type_doc = type_doc
    @classmethod
    def clean(cls, filename):
        if(cls._type_doc == 'csv'):
            train = pd.read_csv(filename, encoding='utf-8')
        else:
            train = pd.read_excel(filename)
        train.text = train.text.astype(str)
        df = pd.concat([train])
        df['text'] = df['text'].apply(cls.__pr.preprocess_text)
        train = df[~df['question'].isna()]
        train['question'] = train['question'].astype(int)
        if (cls._type_doc == "csv"):
            train.to_csv(filename, index=False)
        else:
            train.to_excel(filename, index=False)

class CommandCleaner(ICleaner):
    __pr = TextPreprocessers.CommandPreprocessing()
    _type_doc = 'xlsx'
    def __init__(self, type_doc):
        CommandCleaner._type_doc = type_doc
    @classmethod
    def clean(cls, filename):
        
        if(cls.type_doc == 'csv'):
            train = pd.read_csv(filename, encoding='utf-8')
        else:
            train = pd.read_excel(filename)
        train.text = train.text.astype(str)
        df = pd.concat([train])
        df['text'] = df['text'].apply(cls.__pr.preprocess_text)
        train = df[~df['command'].isna()]
        train['command'] = train['command'].astype(int)
        if (cls._type_doc == 'csv'):
            train.to_csv(filename, index=False)
        else:
            train.to_excel(filename, index=False)
