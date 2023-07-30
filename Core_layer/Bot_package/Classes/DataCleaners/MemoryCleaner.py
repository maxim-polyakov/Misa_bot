from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.DB_Bridge import DB_Communication
from Core_layer.Bot_package.Interfaces import ICleaner


class MemoryCleaner(ICleaner.ICleaner):
    __pr = CommonPreprocessing.CommonPreprocessing()
    dbname = None

    def __init__(self, dbname):
        MemoryCleaner.dbname = dbname

    @classmethod
    def clean(cls):
        df = DB_Communication.DB_Communication.get_data(
            'SELECT * from train_sets.' + cls.dbname)
        df['text'] = df['text'].apply(cls.__pr.preprocess_text)
        print(df['text'])
        DB_Communication.DB_Communication.delete_data('DELETE FROM train_sets.' + cls.dbname)

        DB_Communication.DB_Communication.insert_to(df, cls.dbname, 'train_sets')
