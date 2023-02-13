from Deep_layer.DB_package import DB_Bridge
from Core_layer.Test_package.TestMonitors import TestMonitor

class TestMonitorLSTM(TestMonitor.TestMonitor):

    @classmethod
    def monitor(cls):

        DB_Bridge.DB_Communication.delete_data(
            'DELETE FROM validation_sets.markedvalidsetlstm')

        df = DB_Bridge.DB_Communication.get_data(
            'SELECT id, text from validation_sets.markedvalidsethuman ORDER BY id ASC')

        datatable = 'markedvalidsetlstm'

        modelpath = '/binary/LSTM/'

        super().monitor(df, datatable, modelpath)