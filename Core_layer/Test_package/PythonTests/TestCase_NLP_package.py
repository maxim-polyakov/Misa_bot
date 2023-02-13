from Core_layer.Test_package.PythonTests import ITestCase
from Deep_layer.NLP_package.Models.Binary import NaiveBayes
import unittest

class TestCase_NLP_package(ITestCase.ITestCase):

    def test_nbmodel_train(self):
        # filemodel = next(Path().rglob('0_himodel.h5'))
        # filetokenizer = next(Path().rglob('0_hitokenizer.pickle'))
        # datasetfile = cls.sel.SELECT_HI
        #
        # nbmodel = NaiveBayes.NaiveBayes()
        pass

if __name__ == '__main__':
    unittest.main()
