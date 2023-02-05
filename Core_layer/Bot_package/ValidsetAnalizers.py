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

        outdict = {'LSTMACC':[], 'RandomForestAcc': [], "NaiveBayesAcc": [], "XGBoostAcc":[], "CombineAcc": []}

        DB_Bridge.DB_Communication.delete_data('DELETE FROM assistant_sets.analyzetable')

        humandf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsethuman ORDER BY id ASC')
        lstmdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetlstm ORDER BY id ASC')
        nbdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetnaivebayes ORDER BY id ASC')
        rfdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetrandomforest ORDER BY id ASC')
        xbdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetxgboost ORDER BY id ASC')
        combinedf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets.markedvalidsetcombine ORDER BY id ASC')

        rdf = DB_Bridge.pd.DataFrame(
            {'id': humandf['id'], 'text': humandf['text'], 'agendaLSTM': lstmdf['agenda'], 'agendaRandomForest': rfdf['agenda'],
             'agendaNaiveBayes': nbdf['agenda'], 'agendaXGBoost': xbdf['agenda'], 'agendaCombine': combinedf['agenda'],
             'agendaHuman': humandf['agenda']})
        DB_Bridge.DB_Communication.insert_to(rdf, 'analyzetable')

        df = DB_Bridge.DB_Communication.get_data('select distinct * '
                                                             'from assistant_sets.analyzetable '
                                                             'where \"agendaHuman\" not like "Команда" ' 
                                                             'and \"agendaCombine\" is not null ' 
                                                             'and \"agendaNaiveBayes\" is not null ' 
                                                             'and \"agendaLSTM\" is not null ' 
                                                             'and \"agendaRandomForest\" is not null '
                                                             'and \"agendaXGBoost\" is not null')

        outdict['LSTMACC'].append(str(accuracy_score(df['agendaLSTM'], df['agendaHuman'])))
        outdict['RandomForestAcc'].append(str(accuracy_score(df['agendaRandomForest'], df['agendaHuman'])))
        outdict['NaiveBayesAcc'].append(str(accuracy_score(df['agendaNaiveBayes'], df['agendaHuman'])))
        outdict['XGBoostAcc'].append(str(accuracy_score(df['agendaXGBoost'], df['agendaHuman'])))
        outdict['CombineAcc'].append(str(accuracy_score(df['agendaCombine'], df['agendaHuman'])))

        return outdict


    @classmethod
    @dispatch(object, object)
    def analize(cls, analyzetable):

        outdict = {'LSTMACC': [], 'RandomForestAcc': [], 'NaiveBayesAcc': [], 'XGBoostAcc': [], 'CombineAcc': []}

        df = DB_Bridge.DB_Communication.get_data('select distinct * '
                                                             'from assistant_sets.analyzetable '
                                                             'where \"agendaHuman\" not like "Команда" ' 
                                                             'and \"agendaCombine\" is not null ' 
                                                             'and \"agendaNaiveBayes\" is not null ' 
                                                             'and \"agendaLSTM\" is not null ' 
                                                             'and \"agendaRandomForest\" is not null '
                                                             'and \"agendaXGBoost\" is not null')


        outdict['LSTMACC'].append(str(accuracy_score(df['agendaLSTM'], df['agendaHuman'])))
        outdict['RandomForestAcc'].append(str(accuracy_score(df['agendaRandomForest'], df['agendaHuman'])))
        outdict['NaiveBayesAcc'].append(str(accuracy_score(df['agendaNaiveBayes'], df['agendaHuman'])))
        outdict['XGBoostAcc'].append(str(accuracy_score(df['agendaXGBoost'], df['agendaHuman'])))
        outdict['CombineAcc'].append(str(accuracy_score(df['agendaCombine'], df['agendaHuman'])))

        return outdict
