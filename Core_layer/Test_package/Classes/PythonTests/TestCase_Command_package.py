#from Core_layer.Bot_package.Classes.ValidsetAnalizers import ValidsetAlanizer as va
from Core_layer.Bot_package.Classes.DataCleaners import MemoryCleaner as ma
from Core_layer.Bot_package.Classes.Bototrainers import LSTMtrain
from Core_layer.Bot_package.Classes.ValidsetAnalizers import ValidsetAlanizer as va
from Core_layer.Test_package.Interfases import ITestCase
import unittest

class TestCase_CommandAction(ITestCase.ITestCase):


    """

    This class is written for testing an entityes of system

    """
    validsetanalizer = va.ValidsetAlanizer()


    def test_bridge_analizer(self):
        self.validsetanalizer.analyze()
        self.assertEqual()

    def test_bridge_clean(self):
        memoryCleaner = ma.MemoryCleaner('all_set_business')
        memoryCleaner.clean()
        self.assertEqual()

    def test_hitrain(self):
        lstmtrain = LSTMtrain.LSTMtrain()
        lstmtrain.hitrain(30)
        self.assertEqual()
    def test_trashtrain(self):
        self.assertEqual()

    def test_trashtrain(self):
        self.assertEqual()

    def test_thtrain(self):
        self.assertEqual()

    def test_emotionstrain(self):
        self.assertEqual()

    def test_weathertrain(self):
        self.assertEqual()

    def test_businesstrain(self):
        self.assertEqual()

class TestCase_CommandAnalyzer(ITestCase.ITestCase):


    """

    This class is written for testing an entityes of system

    """
    validsetanalizer = va.ValidsetAlanizer()

    def test_bridge(self):
        self.validsetanalizer.analyze()
        self.assertNotEqual()

if __name__ == '__main__':
    unittest.main()
