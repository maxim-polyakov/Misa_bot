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
        outdict = {'LSTMACC': []}

        humandf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsethuman ORDER BY id ASC')
        lstmdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetlstm ORDER BY id ASC')

        rdf = DB_Bridge.pd.DataFrame(
            {'id': humandf['id'], 'text': humandf['text'], 'agendalstm': lstmdf['agenda'], 'agendahuman': humandf['agenda']})

        DB_Bridge.DB_Communication.delete_data('DELETE FROM assistant_sets.analyzetable')

        DB_Bridge.DB_Communication.insert_to(rdf, 'analyzetable')

        select = str("select distinct * from assistant_sets.analyzetable " +
                     "where agendahuman  not like 'Команда' " +
                     "and agendalstm is not null ")

        df = DB_Bridge.DB_Communication.get_data(select)

        outdict['LSTMACC'].append(str(accuracy_score(df['agendalstm'], df['agendahuman'])))
        return outdict

    @classmethod
    @dispatch(object, object)
    def analize(cls, analyzetable):
        outdict = {'LSTMACC': []}

        select = str("select distinct * from assistant_sets.analyzetable " +
                     "where agendahuman  not like 'Команда' " +
                     "and agendalstm is not null ")

        df = DB_Bridge.DB_Communication.get_data(select)

        outdict['LSTMACC'].append(str(accuracy_score(df['agendalstm'], df['agendahuman'])))
        return outdict
