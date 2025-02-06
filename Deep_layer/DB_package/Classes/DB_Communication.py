import logging
import warnings
import pandas as pd
from multipledispatch import dispatch
from Deep_layer.DB_package.Classes import Connections
from Deep_layer.DB_package.Inerfaces import IDB_Communication
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing


class DB_Communication(IDB_Communication.IDB_Communication):
    """
    It is class for communication with a data base
    """
    warnings.filterwarnings('ignore')
    @classmethod
    @dispatch(object, object, object, object, object, object, object)
    def insert_to(cls, text, tablename, string, agenda, classification, classtype):
        # inserting data to a database
        # setting up logging configuration
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # establishing a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            # creating an instance of the preprocessing class
            pr = CommonPreprocessing.CommonPreprocessing()
            # preparing the data dictionary with preprocessed text and other parameters
            data = {'text': pr.preprocess_text(
                text), agenda: string, classification: classtype}
            # creating an empty dataframe
            df = pd.DataFrame()
            # creating a new row from the data dictionary
            new_row = pd.Series(data)
            # appending the new row to the dataframe
            df = df.append(new_row, ignore_index=True)
            # log that the insertion process is completed
            logging.info('The db_communication.insert_to 1 is done')
            # inserting the dataframe into the specified table in the database
            df.to_sql(tablename, con=postgr_conn.engine_remote,
                schema='recognized_sets', index=False, if_exists='append')
        except Exception as e:
            logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, int, object, object, object)
    def insert_to(cls, idx, txt, insert, datatable):
        # inserting data to a database
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # establish a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            # split the 'insert' parameter into a list using ', ' as a delimiter
            insert = insert.split(', ')
            # create a dictionary with the data to be inserted
            data = {'id': idx, 'text': txt, 'agenda': insert[0], 'emotion': insert[1]}
            # create an empty dataframe
            df = pd.DataFrame()
            # create a new row from the dictionary
            new_row = pd.Series(data)
            # append the new row to the dataframe
            df = df.append(new_row, ignore_index=True)
            # log that the insertion process is completed
            logging.info('The db_communication.insert_to 2 is done')
            # insert the dataframe into the specified database table
            df.to_sql(datatable, con=postgr_conn.engine_remote, schema='validation_sets',
                index=False, if_exists='append')
        except Exception as e:
            # log any exceptions that occur during the process
            logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, object, object, object)
    def insert_to(cls, df, datatable, schema):
        # inserting data to a database
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # establish a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            # log that the insertion process is completed
            logging.info('The db_communication.insert_to 3 is done')
            # insert the dataframe into the specified database table
            df.to_sql(datatable, con=postgr_conn.engine_remote, schema=schema,
                index=False, if_exists='append')
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, object, object)
    def insert_to(cls, df, datatable):
        # inserting data to a database
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # establish a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            # log that the insertion process is completed
            logging.info('The db_communication.insert_to 4 is done')
            # insert the dataframe into the specified table in the database
            df.to_sql(datatable, con=postgr_conn.engine_remote, schema='assistant_sets',
                index=False, if_exists='append')
        except Exception as e:
            logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, str, str)
    def insert_to(cls, string, datatable):
        # inserting data to a database
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # establish a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            # retrieve the current count of tokens from the specified table
            dfvalid = pd.read_sql('select count(tokens) from assistant_sets.' + datatable,
                            postgr_conn.conn_remote)
            # get the count value
            count = dfvalid['count'][0]
            # prepare the data to be inserted
            data = {'id': count + 1, 'token': string}
            # create an empty dataframe
            df = pd.DataFrame()
            # create a new row with the data
            new_row = pd.Series(data)
            # append the new row to the dataframe
            df = df.append(new_row, ignore_index=True)
            # log that the insertion process is completed
            logging.info('The db_communication.insert_to 5 is done')
            # insert the dataframe into the specified table in the database
            df.to_sql(datatable, con=postgr_conn.engine_remote, schema='assistant_sets',
                        index=False, if_exists='append')
        except Exception as e:
            # log any exceptions that occur during the process
            logging.exception(str('The exception is in db_communication.insert_to ' + str(e)))

    @classmethod
    @dispatch(object, object)
    def insert_to(cls, lowertext):
        # inserting data to a database
        # setting up logging configuration
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # establishing a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            def insert(table, count, text, schema):
                # iterating through the text list and inserting each entry into the database
                for txt in text:
                    data = {'id': count + 1,'text': txt}
                    df = pd.DataFrame()
                    new_row = pd.Series(data)
                    df = df.append(new_row, ignore_index=True)
                    # log that the insertion process is completed
                    logging.info('The db_communication.insert_to 6 is done')
                    # inserting the dataframe into the database table
                    df.to_sql(table, con=postgr_conn.engine_remote, schema=schema,
                        index=False, if_exists='append')

            # cleaning the input text (this part seems redundant)
            lowertext = lowertext.replace('миса ', '').replace('misa ', '')
            text = []
            # retrieving the current count of text entries from the database
            dfmesstor = pd.read_sql('select count(text) from messtorage.storage',
                            postgr_conn.conn_remote)
            counts = dfmesstor['count'][0]
            text.append(lowertext)
            # calling the insert function to insert data into the database
            insert('storage', counts, text, 'messtorage')
        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception(str('The exception is in db_communication.get_data ' + str(e)))

    @classmethod
    def get_data(cls, select):
        # getting data to a database
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # establish a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            # execute the sql query and store the result in a dataframe
            df = pd.read_sql(select, postgr_conn.conn_remote)
            # log a success message
            logging.info('The db_communication.get_data is done')
            return df
        except Exception as e:
            # log an error message if an exception occurs
            logging.exception(str('The exception is in db_communication.get_data ' + str(e)))

    @classmethod
    def delete_data(cls, delete):
        # deleting data to a database
        # setting up logging configuration
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # establishing a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            # creating a cursor object to execute the sql query
            cur = postgr_conn.conn_remote.cursor()
            # executing the delete query
            cur.execute(delete)
            # committing the transaction to apply changes
            postgr_conn.conn_remote.commit()
            # logging successful execution
            logging.info('The db_communication.delete_data is done')
            # closing the cursor
            cur.close()
        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception(str('The exception is in db_communication.delete_data ' + str(e)))

    @classmethod
    def checkcommands(cls, input_string):
        # checking of commands in a database
        # configuring logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # establishing a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            # retrieving the list of commands from the database
            df = pd.read_sql('SELECT text FROM assistant_sets.commands', postgr_conn.conn_remote)
            # converting the retrieved commands into a dictionary
            Cdict = df['text'].to_dict()
            # splitting the input string into an array of words
            input_array = input_string.split(' ')
            # checking if any word in the input string matches a command from the database
            for cdictvalue in Cdict.values():
                for item in input_array:
                    if(cdictvalue == item):
                        # logging and returning true if a match is found
                        logging.info('The db_communication.checkcommands is done')
                        return True
            # logging and returning false if no match is found
            logging.info('The db_communication.checkcommands is done')
            return False
        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception(str('The exception is in db_communication.checkcommands ' + str(e)))

    @classmethod
    def check(cls, input_string, table):
        # checking of table in a database
        # configuring logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # creating an instance of the preprocessing class
            pr = CommonPreprocessing.CommonPreprocessing()
            # establishing a connection to the postgresql database
            postgr_conn = Connections.PostgresConnection()
            # retrieve text data from the specified table in the database
            df = pd.read_sql('SELECT text FROM train_sets.' + table, postgr_conn.conn_remote)
            Cdict = df['text'].to_dict()
            inpt = []
            inpt.append(pr.preprocess_text(input_string[0]))
            # check if any value from the database exists in the preprocessed input
            for cdictvalue in Cdict.values():
                if (cdictvalue in inpt):
                    # logging and returning true if a match is found
                    logging.info('The db_communication.check is done')
                    return True
            # logging and returning false if no match is found
            logging.info(str('The db_communication.check is done'))
            return False
        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception(str('The exception is in db_communication.check ' + str(e)))
