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
        filemodel = str(next(Path().rglob('-1_nbmodetest.pickle')))
        filetokenizer = str(next(Path().rglob('-1_nbtoktest.pickle')))
        datasetfile = self.sel.SELECT_HI
        trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile)
        trainer.train('hi')

    def test_rfmodel_train(self):
        #
        # filemodel = next(Path().rglob('0_himodel.h5'))
        # filetokenizer = './tokenizers/binary/NaiveBayes/hivec.pickle'
        # datasetfile = self.sel.SELECT_HI
        # trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile)
        # trainer.train('hi')
        filemodel = Path().as_posix() + str(next(Path().rglob('-1_rfmodetest.pickle')))

        filetokenizer = str(next(Path().rglob('-1_rftoktest.pickle')))
        datasetfile = self.sel.SELECT_HI
        trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)
        trainer.train('hi')


    def test_xgmodel_train(self):
        pass

if __name__ == '__main__':
    unittest.main()
