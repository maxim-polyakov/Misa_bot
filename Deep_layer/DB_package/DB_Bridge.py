import pandas as pd
from Deep_layer.NLP_package import TextPreprocessers
from multipledispatch import dispatch
from abc import ABC, abstractmethod
import numpy as np
from Deep_layer.DB_package import Connections

class IDB_Communication(ABC):

    @abstractmethod
    def insert_to(cls):
        pass

    @abstractmethod
    def get_data(cls):
        pass

    @abstractmethod
    def delete_data(cls, delete):
        pass

    @abstractmethod
    def checkcommands(cls):
        pass

class DB_Communication(IDB_Communication):

    @classmethod
    @dispatch(object, object, object, object, object, object, object)
    def insert_to(cls, text, tablename, string, agenda, classification, classtype):
        pr = TextPreprocessers.CommonPreprocessing()
        data = {'text': pr.preprocess_text(
            text), agenda: string, classification: classtype}
        df = pd.DataFrame()
        new_row = pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(tablename, con=Connections.PostgresConnection.engine_remote,
                  schema='recognized_sets', index=False, if_exists='append')

    @classmethod
    @dispatch(object, np.int64, object, object, object)
    def insert_to(cls, idx, txt, insert, datatable):
        insert = insert.split(', ')
        data = {'id':idx, 'text': txt, 'agenda': insert[0], 'emotion': insert[1]}
        df = pd.DataFrame()
        new_row = pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(datatable, con=Connections.PostgresConnection.engine_remote, schema='validation_sets',
                  index=False, if_exists='append')

    @classmethod
    @dispatch(object, object, object, object)
    def insert_to(cls, df, datatable, schema):
        df.to_sql(datatable, con=Connections.PostgresConnection.engine_remote, schema=schema,
                  index=False, if_exists='append')

    @classmethod
    @dispatch(object, object, object)
    def insert_to(cls, df, datatable):
       df.to_sql(datatable, con=Connections.PostgresConnection.engine_remote, schema='assistant_sets',
                 index=False, if_exists='append')

    @classmethod
    @dispatch(object, str, str)
    def insert_to(cls, string, datatable):
       dfvalid = pd.read_sql('select count(tokens) from assistant_sets.' + datatable,
                             Connections.PostgresConnection.conn_remote)
       count = dfvalid['count'][0]
       data = {'id': count + 1, 'token': string}
       df = pd.DataFrame()
       new_row = pd.Series(data)
       df = df.append(new_row, ignore_index=True)
       df.to_sql(datatable, con=Connections.PostgresConnection.engine_remote, schema='assistant_sets',
                 index=False, if_exists='append')

    @classmethod
    @dispatch(object, object)
    def insert_to(cls, lowertext):

        def insert(table, count, text, schema):
            for txt in text:
                data = {'id': count + 1,'text': txt}
                df = pd.DataFrame()
                new_row = pd.Series(data)
                df = df.append(new_row, ignore_index=True)
                df.to_sql(table, con=Connections.PostgresConnection.engine_remote, schema=schema,
                          index=False, if_exists='append')

        lowertext = lowertext.replace('миса ', '').replace('misa ', '')
        text = []
        dfvalid = pd.read_sql('select count(text) from validation_sets.markedvalidsethuman',
                              Connections.PostgresConnection.conn_remote)
        counth = dfvalid['count'][0]
        dfmesstor = pd.read_sql('select count(text) from messtorage.storage',
                                Connections.PostgresConnection.conn_remote)
        counts = dfmesstor['count'][0]
        text.append(lowertext)
        insert('storage', counts, text, 'messtorage')
        insert('markedvalidsethuman', counth, text, 'validation_sets')

    @classmethod
    def get_data(cls, select):
        try:
            df = pd.read_sql(select, Connections.PostgresConnection.conn_remote)
            return df
        except:
            print("exception is in DB_Communication.get_data")


    @classmethod
    def delete_data(cls, delete):
        try:
            cur = Connections.PostgresConnection.conn_remote.cursor()
            cur.execute(delete)
            Connections.PostgresConnection.conn_remote.commit()
            cur.close()
        except:
            print("exception is in DB_Communication.get_data")

    @classmethod
    def checkcommands(cls, input_string):
        try:
            df = pd.read_sql('SELECT text FROM assistant_sets.commands', Connections.PostgresConnection.conn_remote)
            Cdict = df['text'].to_dict()
            for cdictvalue in Cdict.values():
                if(cdictvalue in input_string):
                    return True
            return False
        except:
            print("exception is in DB_Communication.checkcommands")