from Core_layer.Test_package.PythonTests import ITestCase
from Deep_layer.NLP_package.Models.Multy import NaiveBayes
#from Deep_layer.NLP_package.Models.Binary import NaiveBayes
#from Deep_layer.NLP_package.Models.Binary import NaiveBayes
from Core_layer.Bot_package import Selects
import unittest

class TestCase_NLP_package(ITestCase.ITestCase):

    sel = Selects.Select()

    def test_nbmodel_train(self):

        filemodel = './models/binary/NaiveBayes/himodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/hivec.pickle'
        datasetfile = self.sel.SELECT_HI
        trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile)
        trainer.train('hi')

    def test_nbmodel_train(self):


        filemodel = './models/binary/NaiveBayes/himodel.pickle'
        filetokenizer = './tokenizers/binary/NaiveBayes/hivec.pickle'
        datasetfile = self.sel.SELECT_HI
        trainer = NaiveBayes.NaiveBayes(filemodel, filetokenizer, datasetfile)
        trainer.train('hi')

if __name__ == '__main__':
    unittest.main()
