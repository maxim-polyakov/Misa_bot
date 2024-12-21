import unittest
from Core_layer.Bot_package.Classes.DataCleaners import MemoryCleaner as ma
from Core_layer.Test_package.Interfases import ITestCase
from Core_layer.Bot_package.Classes.Drawers import Drawer

class TestCase_ValidsetAlanizer(ITestCase.ITestCase):
    """

    This class is written for testing entityes of system

    """
    def test_bingfinder(self):
        dr = Drawer.Drawer("нож")
        return_arr = dr.draw()
        self.assertNotEqual(return_arr, None)
if __name__ == '__main__':
    unittest.main()
