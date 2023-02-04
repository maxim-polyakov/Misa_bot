import unittest
from Deep_layer.API_package import Calculators as calc
from Deep_layer.API_package import Finders as find
from Deep_layer.API_package import Translators as trans
from Deep_layer.DB_package import DB_Bridge as bridge
from Core_layer.Bot_package import ValidsetAnalizers

class TestRun:

  @classmethod
  def run_all_tests(cls):
    #case = MyTestCase()
    #case.test_calc()
    #case.test_founder()
    #case.test_trans()
    #case.test_bridge()
    #case.test_ValidsetAnalizers()
    pass

class MyTestCase(unittest.TestCase):

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
        con.insert_to(data,'test_table')
        self.assertNotEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()
