from Deep_layer.DB_package.DB_Bridge import DB_Communication
from sklearn.metrics import accuracy_score
from multipledispatch import dispatch
from Core_layer.Bot_package.ValidsetAnalizers import IAnalyzer


class ValidsetAlanizer(IAnalyzer.IAnalyzer):

    @classmethod
    @dispatch(object)
    def analyze(cls):
        outdict = {'LSTMACC': []}

        humandf = DB_Communication.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsethuman ORDER BY id ASC')
        lstmdf = DB_Communication.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetlstm ORDER BY id ASC')

        rdf = DB_Communication.pd.DataFrame(
            {'id': humandf['id'], 'text': humandf['text'], 'agendalstm': lstmdf['agenda'], 'agendahuman': humandf['agenda']})

        DB_Communication.DB_Communication.delete_data('DELETE FROM assistant_sets.analyzetable')

        DB_Communication.DB_Communication.insert_to(rdf, 'analyzetable')

        select = str("select distinct * from assistant_sets.analyzetable " +
                     "where agendahuman  not like 'Команда' " +
                     "and agendalstm is not null ")

        df = DB_Communication.DB_Communication.get_data(select)

        outdict['LSTMACC'].append(str(accuracy_score(df['agendalstm'], df['agendahuman'])))
        return outdict

    @classmethod
    @dispatch(object, object)
    def analize(cls, analyzetable):
        outdict = {'LSTMACC': []}

        select = str("select distinct * from assistant_sets.analyzetable " +
                     "where agendahuman  not like 'Команда' " +
                     "and agendalstm is not null ")

        df = DB_Communication.DB_Communication.get_data(select)

        outdict['LSTMACC'].append(str(accuracy_score(df['agendalstm'], df['agendahuman'])))
        return outdict
