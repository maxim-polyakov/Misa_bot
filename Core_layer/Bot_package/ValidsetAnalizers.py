from abc import ABC, abstractmethod
from Deep_layer.DB_package import DB_Bridge
from sklearn.metrics import accuracy_score
from multipledispatch import dispatch


class IAnalizer(ABC):

    @abstractmethod
    def analize(self):
        pass

class ValidsetAlanizer(IAnalizer):

    @classmethod
    @dispatch(object)
    def analize(cls):
        outdict = {'LSTMACC': [], 'RandomForestAcc': [], "NaiveBayesAcc": []}

        humandf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsethuman ORDER BY id ASC')
        lstmdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetlstm ORDER BY id ASC')
        nbdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetnaivebayes ORDER BY id ASC')
        rfdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetrandomforest ORDER BY id ASC')

        rdf = DB_Bridge.pd.DataFrame(
            {'id': humandf['id'], 'text': humandf['text'], 'agendalstm': lstmdf['agenda'], 'agendarandomforest': rfdf['agenda'],
             'agendanaivebayes': nbdf['agenda'], 'agendahuman': humandf['agenda']})

        DB_Bridge.DB_Communication.delete_data('DELETE FROM assistant_sets.analyzetable')

        DB_Bridge.DB_Communication.insert_to(rdf, 'analyzetable')

        select = str("select distinct * from assistant_sets.analyzetable " +
                     "where agendahuman  not like 'Команда' " +
                     "and agendanaivebayes is not null " +
                     "and agendalstm is not null " +
                     "and agendarandomforest is not null")

        df = DB_Bridge.DB_Communication.get_data(select)

        outdict['LSTMACC'].append(str(accuracy_score(df['agendalstm'], df['agendahuman'])))
        outdict['RandomForestAcc'].append(str(accuracy_score(df['agendarandomforest'], df['agendahuman'])))
        outdict['NaiveBayesAcc'].append(str(accuracy_score(df['agendanaivebayes'], df['agendahuman'])))
        return outdict

    @classmethod
    @dispatch(object, object)
    def analize(cls, analyzetable):
        outdict = {'LSTMACC': [], 'RandomForestAcc': [], 'NaiveBayesAcc': []}

        select = str("select distinct * from assistant_sets.analyzetable " +
                     "where agendahuman  not like 'Команда' " +
                     "and agendanaivebayes is not null " +
                     "and agendalstm is not null " +
                     "and agendarandomforest is not null")

        df = DB_Bridge.DB_Communication.get_data(select)

        outdict['LSTMACC'].append(str(accuracy_score(df['agendalstm'], df['agendahuman'])))
        outdict['RandomForestAcc'].append(str(accuracy_score(df['agendarandomforest'], df['agendahuman'])))
        outdict['NaiveBayesAcc'].append(str(accuracy_score(df['agendanaivebayes'], df['agendahuman'])))
        return outdict
