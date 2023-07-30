from Deep_layer.DB_package.DB_Bridge import DB_Communication
from Core_layer.Test_package.TestMonitors import TestMonitor
from Deep_layer.NLP_package.Predictors import MultyLSTM, RandomForest, NaiveBayes, XGBoost
from Deep_layer.NLP_package.Classes.Predictors import BinaryLSTM


class TestMonitorRF(TestMonitor.TestMonitor):

    @classmethod
    def monitor(cls):

        DB_Communication.DB_Communication.delete_data(
            'DELETE FROM validation_sets.markedvalidsetrandomforest')

        df = DB_Communication.DB_Communication.get_data(
            'SELECT id, text from validation_sets.markedvalidsethuman ORDER BY id ASC')

        datatable = 'markedvalidsetrandomforest'

        modelpath = '/binary/RandomForest/'

        super().setvariables(RandomForest.RandomForest(), MultyLSTM.MultyLSTM())
        super().monitor(df, datatable, modelpath)
