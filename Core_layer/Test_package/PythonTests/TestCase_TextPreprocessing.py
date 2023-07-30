from Core_layer.Test_package.PythonTests import ITestCase
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
import unittest

class TestCase_TextPreprocessing(ITestCase.ITestCase):

    def test_nbmodel_train(self):
        pr = CommonPreprocessing.CommonPreprocessing()
        pr.preprocess_text("покажи данные")
        # cl = MemoryCleaner.MemoryCleaner('all_set_trash')
        # cl.clean()


if __name__ == '__main__':
    unittest.main()