import unittest
import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Test_package.Interfases import ITestCase


class TestCase_API_package(ITestCase.ITestCase):
    """

    This class is written for testing an entityes of system

    """
    pr = CommonPreprocessing.CommonPreprocessing()

    def test_commonpreprocessing(self):
        res = self.pr.preprocess_text('поздоровайся')
        self.assertEqual(res, 'поздороваться')

    def test_gpt(self):
        pass
if __name__ == '__main__':
    unittest.main()
