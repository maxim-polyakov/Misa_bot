import unittest
from Core_layer.Test_package.Interfases import ITestCase
from Deep_layer.IOD_package.Classes import Dalle

class TestCase_IOD_package(ITestCase.ITestCase):
    """

    This class is written for testing entityes of system

    """
    dal = Dalle.Dalle()

    def test_dalle(self):
        res = self.dal.generate('кота')
        self.assertNotEqual(res, None)

if __name__ == '__main__':
    unittest.main()
