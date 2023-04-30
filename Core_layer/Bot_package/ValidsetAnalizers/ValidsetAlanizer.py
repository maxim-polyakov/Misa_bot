from Deep_layer.DB_package.DB_Bridge import DB_Communication
from sklearn.metrics import accuracy_score
from multipledispatch import dispatch
from Core_layer.Bot_package.ValidsetAnalizers import IAnalyzer


class ValidsetAlanizer(IAnalyzer.IAnalyzer):

    @classmethod
    @dispatch(object)
    def analyze(cls):
        outdict = {'LSTMACC': [], 'RFACC': [], 'NBACC': [], 'XGBACC': []}

        humandf = DB_Communication.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsethuman ORDER BY id ASC')

        lstmdf = DB_Communication.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetlstm ORDER BY id ASC')

        rfdf = DB_Communication.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetrandomforest ORDER BY id ASC')

        nbdf = DB_Communication.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetnaivebayes ORDER BY id ASC')

        xgbdf = DB_Communication.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetxgboost ORDER BY id ASC')

        rdf = DB_Communication.pd.DataFrame({
             'id': humandf['id'],
             'text': humandf['text'],
             'agendalstm': lstmdf['agenda'],
             'agendarf': rfdf['agenda'],
             'agendanb': nbdf['agenda'],
             'agendaxgb': xgbdf['agenda'],
             'agendahuman': humandf['agenda']
             })

        DB_Communication.DB_Communication.delete_data('DELETE FROM assistant_sets.analyzetable')

        DB_Communication.DB_Communication.insert_to(rdf, 'analyzetable')

        select = str("select distinct * from assistant_sets.analyzetable " +
                     "where agendalstm " +
                     "not like 'Команда' is not null " +
                     "and agendanb  is not null " +
                     "and agendalstm  is not null " +
                     "and agendarf  is not null " +
                     "and agendaxgb is not null")

        df = DB_Communication.DB_Communication.get_data(select)

        outdict['LSTMACC'].append(str(accuracy_score(df['agendalstm'], df['agendahuman'])))
        outdict['RFACC'].append(str(accuracy_score(df['agendarf'], df['agendahuman'])))
        outdict['NBACC'].append(str(accuracy_score(df['agendanb'], df['agendahuman'])))
        outdict['XGBACC'].append(str(accuracy_score(df['agendaxgb'], df['agendahuman'])))

        return outdict

    @classmethod
    @dispatch(object, object)
    def analize(cls, analyzetable):
        outdict = {'LSTMACC': [], 'RFACC': [], 'NBACC': [], 'XGBACC': []}

        select = str("select distinct * from assistant_sets.analyzetable " +
                     "where agendahuman  not like 'Команда' " +
                     "and agendalstm is not null ")

        df = DB_Communication.DB_Communication.get_data(select)

        outdict['LSTMACC'].append(str(accuracy_score(df['agendalstm'], df['agendahuman'])))
        outdict['RFACC'].append(str(accuracy_score(df['agendarf'], df['agendahuman'])))
        outdict['NBACC'].append(str(accuracy_score(df['agendanb'], df['agendahuman'])))
        outdict['XGBACC'].append(str(accuracy_score(df['agendaxgb'], df['agendahuman'])))

        return outdict
