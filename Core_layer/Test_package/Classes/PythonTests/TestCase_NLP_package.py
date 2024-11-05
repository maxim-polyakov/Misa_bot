import unittest
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Test_package.Interfases import ITestCase
import logging

class TestCase_API_package(ITestCase.ITestCase):

    pr = CommonPreprocessing.CommonPreprocessing()

    def test_commonpreprocessing(self):
        res = self.pr.preprocess_text('поздоровайся')
        self.assertEqual(res, 'поздороваться')


if __name__ == '__main__':
    unittest.main()
