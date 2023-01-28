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
            'SELECT id, text, agenda from validation_sets."markedvalidsetHuman" mh ORDER BY id ASC')
        lstmdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetLSTM" ml ORDER BY id ASC')

        nbdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetNaiveBayes" mnb ORDER BY id ASC')

        rfdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetRandomForest" mrf ORDER BY id ASC')

        xbdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetXGBoost" mx ORDER BY id ASC')

        combinedf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetCombine" mc ORDER BY id ASC')

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

        DB_Bridge.DB_Communication.delete_data('DELETE FROM assistant_sets.analyzetable')

        outdict = {'LSTMACC': [], 'RandomForestAcc': [], 'NaiveBayesAcc': [], 'XGBoostAcc': [], 'CombineAcc': []}

        humandf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetHuman" mh ORDER BY text ASC')
        lstmdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetLSTM" ml ORDER BY text ASC')

        nbdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetNaiveBayes" mnb ORDER BY text ASC')

        rfdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetRandomForest" mrf ORDER BY text ASC')

        xbdf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetXGBoost" mx ORDER BY text ASC')

        combinedf = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetCombine" mc ORDER BY text ASC')

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
