#from Core_layer.Bot_package.Classes.ValidsetAnalizers import ValidsetAlanizer as va
from Core_layer.Bot_package.Classes.DataCleaners import MemoryCleaner as ma
from Core_layer.Test_package.Interfases import ITestCase
import unittest

class TestCase_ValidsetAlanizer(ITestCase.ITestCase):
    """

    Summary

    """
    #validsetanalizer = va.ValidsetAlanizer()


    def test_bridge(self):

        self.validsetanalizer.analyze()

    def test_bridge(self):
        memoryCleaner = ma.MemoryCleaner('all_set_business')
        memoryCleaner.clean()
      #  self.assertNotEqual()


if __name__ == '__main__':
    unittest.main()