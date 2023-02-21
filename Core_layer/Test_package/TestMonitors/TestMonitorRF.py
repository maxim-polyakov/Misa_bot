from Deep_layer.DB_package.DB_Bridge import DB_Communication
from Core_layer.Test_package.TestMonitors import TestMonitor

class TestMonitorRF(TestMonitor.TestMonitor):

    @classmethod
    def monitor(cls):

        DB_Communication.DB_Communication.delete_data(
            'DELETE FROM validation_sets.markedvalidsetrandomforest')

        df = DB_Communication.DB_Communication.get_data(
            'SELECT id, text from validation_sets.markedvalidsethuman ORDER BY id ASC')

        datatable = 'markedvalidsetrandomforest'

        modelpath = '/binary/RandomForest/'

        super().monitor(df, datatable, modelpath)