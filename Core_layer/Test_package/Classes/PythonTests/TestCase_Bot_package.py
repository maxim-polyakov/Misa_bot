#from Core_layer.Bot_package.Classes.ValidsetAnalizers import ValidsetAlanizer as va
from Core_layer.Bot_package.Classes.DataCleaners import MemoryCleaner as ma
from Core_layer.Bot_package.Classes.Bototrainers import LSTMtrain
from Core_layer.Bot_package.Classes.ValidsetAnalizers import ValidsetAlanizer as va
from Core_layer.Test_package.Interfases import ITestCase
import unittest

class TestCase_ValidsetAlanizer(ITestCase.ITestCase):


    """

    This class is written for testing an entityes of system

    """
    validsetanalizer = va.ValidsetAlanizer()


    def test_bridge(self):
        self.validsetanalizer.analyze()

    def test_bridge(self):
        memoryCleaner = ma.MemoryCleaner('all_set_business')
        memoryCleaner.clean()
        self.assertEqual()

    def test_hitrain(self):
        lstmtrain = LSTMtrain.LSTMtrain()
        lstmtrain.hitrain(30)

if __name__ == '__main__':
    unittest.main()
