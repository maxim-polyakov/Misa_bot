from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Test_package.Classes.TestMonitors import TestMonitor
from Deep_layer.NLP_package.Predictors import MultyLSTM
from Deep_layer.NLP_package.Classes.Predictors import BinaryLSTM


class TestMonitorLSTM(TestMonitor.TestMonitor):


    """

    This class describes testing a test variant of message monitor on base LSTM

    """
    @classmethod
    def monitor(cls):

        DB_Communication.DB_Communication.delete_data(
            'DELETE FROM validation_sets.markedvalidsetlstm')

        df = DB_Communication.DB_Communication.get_data(
            'SELECT id, text from validation_sets.markedvalidsethuman ORDER BY id ASC')

        datatable = 'markedvalidsetlstm'

        modelpath = '/binary/LSTM/'

        super().setvariables(BinaryLSTM.BinaryLSTM(), MultyLSTM.MultyLSTM())
        super().monitor(df, datatable, modelpath)
