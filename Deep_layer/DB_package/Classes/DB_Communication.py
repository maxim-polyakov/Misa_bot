import logging
import pandas as pd
from multipledispatch import dispatch
from Deep_layer.DB_package.Classes import Connections
from Deep_layer.DB_package.Inerfaces import IDB_Communication
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing


class DB_Communication(IDB_Communication.IDB_Communication):
    """
    It is class for communication with a data base
    """
    @classmethod
    @dispatch(object, object, object, object, object, object, object)
    def insert_to(cls, text, tablename, string, agenda, classification, classtype):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            postgr_conn = Connections.PostgresConnection()
            pr = CommonPreprocessing.CommonPreprocessing()
            data = {'text': pr.preprocess_text(
                text), agenda: string, classification: classtype}
            df = pd.DataFrame()
            new_row = pd.Series(data)
            df = df.append(new_row, ignore_index=True)
            logging.info('The db_communication.insert_to 1 is done')
            df.to_sql(tablename, con=postgr_conn.engine_remote,
                schema='recognized_sets', index=False, if_exists='append')
        except Exception as e:
            logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, int, object, object, object)
    def insert_to(cls, idx, txt, insert, datatable):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            postgr_conn = Connections.PostgresConnection()
            insert = insert.split(', ')
            data = {'id': idx, 'text': txt, 'agenda': insert[0], 'emotion': insert[1]}
            df = pd.DataFrame()
            new_row = pd.Series(data)
            df = df.append(new_row, ignore_index=True)
            logging.info('The db_communication.insert_to 2 is done')
            df.to_sql(datatable, con=postgr_conn.engine_remote, schema='validation_sets',
                index=False, if_exists='append')
        except Exception as e:
            logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, object, object, object)
    def insert_to(cls, df, datatable, schema):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            postgr_conn = Connections.PostgresConnection()
            logging.info('The db_communication.insert_to 3 is done')
            df.to_sql(datatable, con=postgr_conn.engine_remote, schema=schema,
                index=False, if_exists='append')
        except Exception as e:
            logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, object, object)
    def insert_to(cls, df, datatable):
#
#
       logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
       try:
            postgr_conn = Connections.PostgresConnection()
            logging.info('The db_communication.insert_to 4 is done')
            df.to_sql(datatable, con=postgr_conn.engine_remote, schema='assistant_sets',
                index=False, if_exists='append')
       except Exception as e:
           logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, str, str)
    def insert_to(cls, string, datatable):
#
#
       logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
       try:
            postgr_conn = Connections.PostgresConnection()
            dfvalid = pd.read_sql('select count(tokens) from assistant_sets.' + datatable,
                            postgr_conn.conn_remote)
            count = dfvalid['count'][0]
            data = {'id': count + 1, 'token': string}
            df = pd.DataFrame()
            new_row = pd.Series(data)
            df = df.append(new_row, ignore_index=True)
            logging.info('The db_communication.insert_to 5 is done')
            df.to_sql(datatable, con=postgr_conn.engine_remote, schema='assistant_sets',
                        index=False, if_exists='append')
       except Exception as e:
           logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, object)
    def insert_to(cls, lowertext):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            postgr_conn = Connections.PostgresConnection()
            def insert(table, count, text, schema):
                for txt in text:
                    data = {'id': count + 1,'text': txt}
                    df = pd.DataFrame()
                    new_row = pd.Series(data)
                    df = df.append(new_row, ignore_index=True)
                    logging.info('The db_communication.insert_to 6 is done')
                    df.to_sql(table, con=postgr_conn.engine_remote, schema=schema,
                        index=False, if_exists='append')
            lowertext = lowertext.replace('миса ', '').replace('misa ', '')
            text = []
            dfmesstor = pd.read_sql('select count(text) from messtorage.storage',
                            postgr_conn.conn_remote)
            counts = dfmesstor['count'][0]
            text.append(lowertext)
            insert('storage', counts, text, 'messtorage')
        except Exception as e:
            logging.exception(str('The exception is in db_communication.get_data ' + str(e)))

    @classmethod
    def get_data(cls, select):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            postgr_conn = Connections.PostgresConnection()
            df = pd.read_sql(select, postgr_conn.conn_remote)
            logging.info('The db_communication.get_data is done')
            return df
        except Exception as e:
            logging.exception(str('The exception is in db_communication.get_data ' + str(e)))

    @classmethod
    def delete_data(cls, delete):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            postgr_conn = Connections.PostgresConnection()

            cur = postgr_conn.conn_remote.cursor()
            cur.execute(delete)
            postgr_conn.conn_remote.commit()
            logging.info('The db_communication.delete_data is done')
            cur.close()
        except Exception as e:
            logging.exception(str('The exception is in db_communication.delete_data ' + str(e)))

    @classmethod
    def checkcommands(cls, input_string):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            postgr_conn = Connections.PostgresConnection()
            df = pd.read_sql('SELECT text FROM assistant_sets.commands', postgr_conn.conn_remote)
            Cdict = df['text'].to_dict()
            for cdictvalue in Cdict.values():
                if(cdictvalue in input_string):
                    logging.info('The db_communication.checkcommands is done')
                    return True
            logging.info('The db_communication.checkcommands is done')
            return False
        except Exception as e:
            logging.exception(str('The exception is in db_communication.checkcommands ' + str(e)))

    @classmethod
    def check(cls, input_string, table):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pr = CommonPreprocessing.CommonPreprocessing()
            postgr_conn = Connections.PostgresConnection()
            df = pd.read_sql('SELECT text FROM train_sets.' + table, postgr_conn.conn_remote)
            Cdict = df['text'].to_dict()
            inpt = []
            inpt.append(pr.preprocess_text(input_string[0]))
            for cdictvalue in Cdict.values():
                if (cdictvalue in inpt):
                    logging.info('The db_communication.check is done')
                    return True
            logging.info(str('The db_communication.check is done'))
            return False
        except Exception as e:
            logging.exception(str('The exception is in db_communication.check ' + str(e)))