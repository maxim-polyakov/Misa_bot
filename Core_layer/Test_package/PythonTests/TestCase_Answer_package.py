from Core_layer.Test_package.TestMonitors import TestMonitorLSTM as tmon
from Core_layer.Answer_package.Answers.Classes import QuestionAnswer as answ
from Core_layer.Test_package.PythonTests import ITestCase
import unittest

class TestCase_API_package(ITestCase.ITestCase):

    testmonlstm = tmon.TestMonitorLSTM()
    answer = answ.QuestionAnswer()

    def test_tmon(self):
        self.testmonlstm.monitor()

    def test_answer(self):
        answer = self.answer.answer('тут?')
        self.assertNotEqual(answer, 'да а что?')

    def test_answer(self):
        answer = self.answer.answer('тут?')



if __name__ == '__main__':
    unittest.main()
