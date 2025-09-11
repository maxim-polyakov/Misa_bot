import unittest
from Core_layer.Answer_package.Classes import RandomAnswer as answc
from Core_layer.Answer_package.Classes import GptAnswer as answq
from Core_layer.Test_package.Interfases import ITestCase

class TestCase_API_package(ITestCase.ITestCase):
    """

    This class is written for testing entityes of system

    """
    answerq = answq.GptAnswer()
    answerc = answc.RandomAnswer()

    def test_tmon(self):
        self.testmonlstm.monitor()

    def test_gpt_answer(self):
        answer = self.answerq.answer('тут?')
        self.assertNotEqual(answer, 'да а что?')

if __name__ == '__main__':
    unittest.main()
