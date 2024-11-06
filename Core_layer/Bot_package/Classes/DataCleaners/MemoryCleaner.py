import logging
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import ICleaner
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing


class MemoryCleaner(ICleaner.ICleaner):
    """
    It is class for cleaning the memory
    """
    __pr = CommonPreprocessing.CommonPreprocessing()
    dbname = None

    def __init__(self, dbname):
        MemoryCleaner.dbname = dbname

    @classmethod
    def clean(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            df = DB_Communication.DB_Communication.get_data(
                'SELECT * from train_sets.' + cls.dbname)
            df['text'] = df['text'].apply(cls.__pr.preprocess_text)
            #print(df['text'])
            DB_Communication.DB_Communication.delete_data('DELETE FROM train_sets.' + cls.dbname)

            DB_Communication.DB_Communication.insert_to(df, cls.dbname, 'train_sets')
            logging.info('The memorycleaner.clean is done')
        except Exception as e:
            logging.exception(str('The exception in memorycleaner.clean ' + str(e)))
