import unittest
from Deep_layer.API_package.Classes.Calculators import SympyCalculator as calc
from Deep_layer.API_package.Classes.Finders import WikiFinder as find
from Deep_layer.API_package.Classes.Finders import BingFinder as bfind
from Deep_layer.API_package.Classes.Finders import GoogleFinder as gfind
from Deep_layer.API_package.Classes.Translators import MemoryTranslator as trans
from Core_layer.Test_package.Interfases import ITestCase


class TestCase_API_package(ITestCase.ITestCase):
    """

    This class is written for testing entityes of system

    """
    math = calc.SympyCalculator()
    found = find.WikiFinder()
    traslated = trans.GoogleTranslator("ru")

    def test_calc(self):
        math = calc.SympyCalculator()
        outputder = math.deravative('x^2', 'x')
        outputint = math.integrate('x^2', 'x^3/3')
        self.assertEqual(outputder, '2*x')
        self.assertEqual(outputint, 'x^3/3')

    def test_wikifinder(self):
        found = find.WikiFinder()
        return_arr = found.find("нож")
        self.assertNotEqual(return_arr, None)

    def test_bingfinder(self):
        found = bfind.BingFinder()
        return_arr = found.find("нож")
        self.assertNotEqual(return_arr, None)

    def test_googlefinder(self):
        found = gfind.GoogleFinder()
        return_arr = found.find("пингвин")
        self.assertNotEqual(return_arr, None)

    def test_trans(self):
        mes = self.traslated.translate("knife")
        dataselect = 'SELECT * FROM ' + 'assistant_sets.for_translate'
        insertdtname = 'translated'
        datasel = self.traslated.translate(dataselect, insertdtname)
        self.assertEqual("нож", mes)
        self.assertEqual("Готово", datasel)

if __name__ == '__main__':
    unittest.main()
