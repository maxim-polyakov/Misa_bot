from Deep_layer.NLP_package import TextPreprocessers
from Deep_layer.DB_package import DB_Bridge
from Core_layer.Bot_package.DataCleaners import Interfaces


class MisaMemoryCleater(Interfaces.ICleaner):
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
