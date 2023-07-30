from Core_layer.Bot_package.ValidsetAnalizers import ValidsetAlanizer as va
from Core_layer.Test_package.Interfases import ITestCase
import unittest

class TestCase_ValidsetAlanizer(ITestCase.ITestCase):
    validsetanalizer = va.ValidsetAlanizer()

    def test_bridge(self):

        self.validsetanalizer.analyze()


if __name__ == '__main__':
    unittest.main()