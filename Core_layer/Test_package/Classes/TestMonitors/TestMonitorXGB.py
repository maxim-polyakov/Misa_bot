from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Test_package.Classes.TestMonitors import TestMonitor
from Deep_layer.NLP_package.Predictors import MultyLSTM, XGBoost


class TestMonitorXGB(TestMonitor.TestMonitor):

    @classmethod
    def monitor(cls):

        DB_Communication.DB_Communication.delete_data(
            'DELETE FROM validation_sets.markedvalidsetxgboost')

        df = DB_Communication.DB_Communication.get_data(
            'SELECT id, text from validation_sets.markedvalidsethuman ORDER BY id ASC')

        datatable = 'markedvalidsetxgboost'

        modelpath = '/binary/XgBoost/'

        super().setvariables(XGBoost.Xgboost(), MultyLSTM.MultyLSTM())
        super().monitor(df, datatable, modelpath)
