from Core_layer import Bot_package


class IAnalizer(Bot_package.ABC):

    @Bot_package.abstractmethod
    def analize(self):
        pass

class ValidsetAlanizer(IAnalizer):

    @classmethod
    @Bot_package.dispatch(object)
    def analize(cls):

        outdict = {'LSTMACC':[], 'RandomForestAcc': [], "NaiveBayesAcc": [], "XGBoostAcc":[], "CombineAcc": []}

        Bot_package.DB_Bridge.DB_Communication.delete_data('DELETE FROM assistant_sets.analyzetable')

        humandf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetHuman" mh ORDER BY id ASC')
        lstmdf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetLSTM" ml ORDER BY id ASC')

        nbdf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetNaiveBayes" mnb ORDER BY id ASC')

        rfdf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetRandomForest" mrf ORDER BY id ASC')

        xbdf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetXGBoost" mx ORDER BY id ASC')

        combinedf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetCombine" mc ORDER BY id ASC')

        rdf = Bot_package.DB_package.pd.DataFrame(
            {'id': humandf['id'], 'text': humandf['text'], 'agendaLSTM': lstmdf['agenda'], 'agendaRandomForest': rfdf['agenda'],
             'agendaNaiveBayes': nbdf['agenda'], 'agendaXGBoost': xbdf['agenda'], 'agendaCombine': combinedf['agenda'],
             'agendaHuman': humandf['agenda']})
        Bot_package.DB_Bridge.DB_Communication.insert_to(rdf, 'analyzetable')

        df = Bot_package.DB_Bridge.DB_Communication.get_data('select distinct * '
                                                             'from assistant_sets.analyzetable '
                                                             'where \"agendaHuman\" not like "Команда" ' 
                                                             'and \"agendaCombine\" is not null ' 
                                                             'and \"agendaNaiveBayes\" is not null ' 
                                                             'and \"agendaLSTM\" is not null ' 
                                                             'and \"agendaRandomForest\" is not null '
                                                             'and \"agendaXGBoost\" is not null')

        outdict['LSTMACC'].append(str(Bot_package.accuracy_score(df['agendaLSTM'], df['agendaHuman'])))
        outdict['RandomForestAcc'].append(str(Bot_package.accuracy_score(df['agendaRandomForest'], df['agendaHuman'])))
        outdict['NaiveBayesAcc'].append(str(Bot_package.accuracy_score(df['agendaNaiveBayes'], df['agendaHuman'])))
        outdict['XGBoostAcc'].append(str(Bot_package.accuracy_score(df['agendaXGBoost'], df['agendaHuman'])))
        outdict['CombineAcc'].append(str(Bot_package.accuracy_score(df['agendaCombine'], df['agendaHuman'])))

        return outdict


    @classmethod
    @Bot_package.dispatch(object, object)
    def analize(cls, analyzetable):

        Bot_package.DB_Bridge.DB_Communication.delete_data('DELETE FROM assistant_sets.analyzetable')

        outdict = {'LSTMACC': [], 'RandomForestAcc': [], 'NaiveBayesAcc': [], 'XGBoostAcc': [], 'CombineAcc': []}

        humandf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetHuman" mh ORDER BY text ASC')
        lstmdf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetLSTM" ml ORDER BY text ASC')

        nbdf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetNaiveBayes" mnb ORDER BY text ASC')

        rfdf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetRandomForest" mrf ORDER BY text ASC')

        xbdf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetXGBoost" mx ORDER BY text ASC')

        combinedf = Bot_package.DB_Bridge.DB_Communication.get_data(
            'SELECT id, text, agenda from validation_sets."markedvalidsetCombine" mc ORDER BY text ASC')

        df = Bot_package.DB_Bridge.DB_Communication.get_data('select distinct * '
                                                             'from assistant_sets.analyzetable '
                                                             'where \"agendaHuman\" not like "Команда" ' 
                                                             'and \"agendaCombine\" is not null ' 
                                                             'and \"agendaNaiveBayes\" is not null ' 
                                                             'and \"agendaLSTM\" is not null ' 
                                                             'and \"agendaRandomForest\" is not null '
                                                             'and \"agendaXGBoost\" is not null')


        outdict['LSTMACC'].append(str(Bot_package.accuracy_score(df['agendaLSTM'], df['agendaHuman'])))
        outdict['RandomForestAcc'].append(str(Bot_package.accuracy_score(df['agendaRandomForest'], df['agendaHuman'])))
        outdict['NaiveBayesAcc'].append(str(Bot_package.accuracy_score(df['agendaNaiveBayes'], df['agendaHuman'])))
        outdict['XGBoostAcc'].append(str(Bot_package.accuracy_score(df['agendaXGBoost'], df['agendaHuman'])))
        outdict['CombineAcc'].append(str(Bot_package.accuracy_score(df['agendaCombine'], df['agendaHuman'])))

        return outdict
