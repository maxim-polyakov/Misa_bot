from Core_layer.Test_package.PythonTests import ITestCase
from Deep_layer.NLP_package.Models.Multy import NaiveBayes
from Deep_layer.NLP_package.Models.Multy import RandomForest
#from Deep_layer.NLP_package.Models.Binary import NaiveBayes
from Core_layer.Bot_package import Selects
import unittest
from pathlib import Path
import os

class TestCase_NLP_package(ITestCase.ITestCase):

    sel = Selects.Select()

    def test_nbmodel_train(self):
        pass

    def test_lstmmodel_train(self):
        filemodelpath = str(Path().as_posix())
        filetokenizerpath = str(Path().as_posix())
        filemodel = filemodelpath + '/Deep_layer/models/testmodels/LSTM/0_himodel.h5'
        filetokenizer = filetokenizerpath + '/Deep_layer/testtokenizers/LSTM/0_hitokenizer.pickle'

        datasetfile = self.sel.SELECT_HI
        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('hi')

    def test_xgmodel_train(self):
        pass

if __name__ == '__main__':
    unittest.main()
