import unittest
from Deep_layer.API_package.Calculators import SympyCalculator as calc
from Deep_layer.API_package.Finders import WikiFinder as find
from Deep_layer.API_package.Translators import GoogleTranslator as trans
from Deep_layer.DB_package.DB_Bridge import DB_Communication as bridge
from Core_layer.Test_package.TestMonitors import TestMonitorLSTM as tmon
from Core_layer.Answer_package.Answers import QuestionAnswer as answ
from Core_layer.Test_package.PythonTests import ITestCase

class TestRun:

  @classmethod
  def run_all_tests(cls):
    #case = MyTestCase()
    #case.test_calc()
    #case.test_founder()
    #case.test_trans()
    #case.test_bridge()
    pass

class MyTestCase(ITestCase.ITestCase):

    def test_calc(self):
        math = calc.SympyCalculator()
        outputder = math.deravative('x^2', 'x')
        outputint = math.integrate('x^2', 'x^3/3')
        self.assertEqual(outputder, '2*x')
        self.assertEqual(outputint, 'x^3/3')

    def test_founder(self):
        found = find.WikiFinder()
        return_arr = found.find("нож")
        self.assertNotEqual(return_arr, None)

    def test_trans(self):
        traslated = trans.GoogleTranslator("ru")
        mes = traslated.translate("knife")
        dataselect = 'SELECT * FROM ' + 'assistant_sets.for_translate'
        insertdtname = 'translated'
        datasel = traslated.translate(dataselect, insertdtname)
        self.assertEqual("нож", mes)
        self.assertEqual("Готово", datasel)

    def test_bridge(self):
        con = bridge.DB_Communication()
        data = con.get_data('SELECT * FROM assistant_sets.test_table')
        con.insert_to(data, 'test_table')
        self.assertNotEqual(len(data), 0)

    def test_tmon(self):
        testmonlstm = tmon.TestMonitorLSTM()
        testmonlstm.monitor()

    def test_answer(self):
        answer = answ.QuestionAnswer()
        answer = answer.answer('тут?')
        self.assertNotEqual(answer, 'да а что?')

if __name__ == '__main__':
    unittest.main()
