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
        # data cleaning
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # retrieve data from the database
            df = DB_Communication.DB_Communication.get_data(
                'SELECT * from train_sets.' + cls.dbname)
            # apply text preprocessing to the 'text' column
            df['text'] = df['text'].apply(cls.__pr.preprocess_text)
            #print(df['text'])
            # delete existing data from the database table
            DB_Communication.DB_Communication.delete_data('DELETE FROM train_sets.' + cls.dbname)
            # insert the cleaned data back into the database
            DB_Communication.DB_Communication.insert_to(df, cls.dbname, 'train_sets')
            # log successful completion of the cleaning process
            logging.info('The memorycleaner.clean process is completed successfully')
        except Exception as e:
            logging.exception('The exception occurred in memorycleaner.clean: ' + str(e))
