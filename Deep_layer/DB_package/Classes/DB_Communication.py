import pandas as pd
from multipledispatch import dispatch
from Deep_layer.DB_package.Classes import Connections
from Deep_layer.DB_package.Inerfaces import IDB_Communication
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
import psycopg2


class DB_Communication(IDB_Communication.IDB_Communication):
    """

    Summary

    """


    @classmethod
    @dispatch(object, object, object, object)
    def insert_to(cls, df, datatable, schema):
#
#
        postgr_conn = Connections.PostgresConnection()
        df.to_sql(datatable, con=postgr_conn.engine_remote, schema=schema,
            index=False, if_exists='append')


#     @classmethod
#     @dispatch(object, object, object)
#     def insert_to(cls, df, datatable):
# #
# #
#        try:
#             postgr_conn = Connections.PostgresConnection()
#             df.to_sql(datatable, con=postgr_conn.engine_remote, schema='assistant_sets',
#                 index=False, if_exists='append')
#        except psycopg2.OperationalError:
#            print("exception is in DB_Communication.insert_to")

    @classmethod
    @dispatch(object, str, str)
    def insert_to(cls, string, datatable):
#
#
       try:
            postgr_conn = Connections.PostgresConnection()
            df = pd.DataFrame()
            df.to_sql(datatable, con=postgr_conn.engine_remote, schema='assistant_sets',
                        index=False, if_exists='append')
       except psycopg2.OperationalError:
           print("exception is in DB_Communication.insert_to")

    @classmethod
    @dispatch(object, object)
    def insert_to(cls, lowertext):
#
#
        try:
            postgr_conn = Connections.PostgresConnection()
            def insert(table, count, text, schema):
                for txt in text:
                    data = {'id': count + 1,'text': txt}
                    df = pd.DataFrame()
                    new_row = pd.Series(data)
                    df = df.append(new_row, ignore_index=True)
                    df.to_sql(table, con=postgr_conn.engine_remote, schema=schema,
                        index=False, if_exists='append')

            lowertext = lowertext.replace('миса ', '').replace('misa ', '')
            text = []
            dfmesstor = pd.read_sql('select count(text) from messtorage.storage',
                            postgr_conn.conn_remote)
            counts = dfmesstor['count'][0]
            text.append(lowertext)
            insert('storage', counts, text, 'messtorage')
        except:
            print("exception is in DB_Communication.get_data")

    @classmethod
    def get_data(cls, select):
#
#
        try:
            postgr_conn = Connections.PostgresConnection()
            df = pd.read_sql(select, postgr_conn.conn_remote)
            return df
        except psycopg2.OperationalError:
            print("exception is in DB_Communication.get_data")


    @classmethod
    def delete_data(cls, delete):
#
#
        try:
            postgr_conn = Connections.PostgresConnection()

            cur = postgr_conn.conn_remote.cursor()
            cur.execute(delete)
            postgr_conn.conn_remote.commit()
            cur.close()
        except psycopg2.OperationalError:
            print("exception is in DB_Communication.delete_data")

    @classmethod
    def checkcommands(cls, input_string):
#
#
        try:
            postgr_conn = Connections.PostgresConnection()
            df = pd.read_sql('SELECT text FROM assistant_sets.commands', postgr_conn.conn_remote)
            Cdict = df['text'].to_dict()
            for cdictvalue in Cdict.values():
                if(cdictvalue in input_string):
                    return True
            return False
        except psycopg2.OperationalError:
            print("exception is in DB_Communication.checkcommands")