import Deep_layer.DB_package as db

class IDB_Communication(db.ABC):

    @db.abstractmethod
    def insert_to(cls):
        pass

    @db.abstractmethod
    def get_data(cls):
        pass

    @db.abstractmethod
    def delete_data(cls, delete):
        pass

    @db.abstractmethod
    def checkcommands(cls):
        pass

class DB_Communication(IDB_Communication):

    @classmethod
    @db.dispatch(object, object, object, object, object, object, object)
    def insert_to(cls, text, tablename, string, agenda, classification, classtype):
        pr = db.TextPreprocessers.CommonPreprocessing()
        data = {'text': pr.preprocess_text(
            text), agenda: string, classification: classtype}
        df = db.pd.DataFrame()
        new_row = db.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(tablename, con=db.Connections.PostgresConnection.engine,
                  schema='recognized_sets', index=False, if_exists='append')

    @classmethod
    @db.dispatch(object, db.np.int64, object, object, object)
    def insert_to(cls, idx, txt, insert, datatable):
        insert = insert.split(', ')
        data = {'id':idx, 'text': txt, 'agenda': insert[0], 'emotion': insert[1]}
        df = db.pd.DataFrame()
        new_row = db.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(datatable, con=db.Connections.PostgresConnection.engine, schema='validation_sets',
                  index=False, if_exists='append')

    @classmethod
    @db.dispatch(object, object, object, object)
    def insert_to(cls, df, datatable, schema):
        df.to_sql(datatable, con=db.Connections.PostgresConnection.engine, schema=schema,
                  index=False, if_exists='append')

    @classmethod
    @db.dispatch(object, object, object)
    def insert_to(cls, df, datatable):
       df.to_sql(datatable, con=db.Connections.PostgresConnection.engine, schema='assistant_sets',
                 index=False, if_exists='append')

    @classmethod
    @db.dispatch(object, str, str)
    def insert_to(cls, string, datatable):
       dfvalid = db.pd.read_sql('select count(tokens) from assistant_sets.' + datatable,
                                         db.Connections.PostgresConnection.conn)
       count = dfvalid['count'][0]
       data = {'id': count + 1, 'token': string}
       df = db.pd.DataFrame()
       new_row = db.pd.Series(data)
       df = df.append(new_row, ignore_index=True)
       df.to_sql(datatable, con=db.Connections.PostgresConnection.engine, schema='assistant_sets',
                 index=False, if_exists='append')

    @classmethod
    @db.dispatch(object, object)
    def insert_to(cls, lowertext):

        def insert(table, count, text, schema):
            for txt in text:
                data = {'id': count + 1,'text': txt}
                df = db.pd.DataFrame()
                new_row = db.pd.Series(data)
                df = df.append(new_row, ignore_index=True)
                df.to_sql(table, con=db.Connections.PostgresConnection.engine, schema=schema,
                          index=False, if_exists='append')


        lowertext = lowertext.replace('миса ', '').replace('misa ', '')
        text = []
        dfvalid = db.pd.read_sql('select count(text) from validation_sets."markedvalidsetHuman" mh',
                                 db.Connections.PostgresConnection.conn)
        counth = dfvalid['count'][0]
        dfmesstor = db.pd.read_sql('select count(text) from messtorage.storage',
                                   db.Connections.PostgresConnection.conn)
        counts = dfmesstor['count'][0]
        text.append(lowertext)
        insert('storage', counts, text, 'messtorage')
        insert('markedvalidsetHuman', counth, text, 'validation_sets')

    @classmethod
    def get_data(cls, select):
        df = db.pd.read_sql(select, db.Connections.PostgresConnection.conn)
        return df

    @classmethod
    def delete_data(cls, delete):
        cur = db.Connections.PostgresConnection.conn.cursor()
        cur.execute(delete)
        db.Connections.PostgresConnection.conn.commit()
        cur.close()
        #DB_package.Connections.PostgresConnection.conn.close()

    @classmethod
    def checkcommands(cls, input_string):
        df = db.pd.read_sql('SELECT text FROM assistant_sets.commands', db.Connections.PostgresConnection.conn)
        Cdict = df['text'].to_dict()
        for cdictvalue in Cdict.values():
            if(cdictvalue in input_string):
                return True
        return False