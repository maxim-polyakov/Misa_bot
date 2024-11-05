import unittest
from Deep_layer.DB_package.Classes import DB_Communication as bridge
from Core_layer.Test_package.Interfases import ITestCase

class TestCase_DB_package(ITestCase.ITestCase):
    """

    This class is written for testing an entityes of system

    """
    con = bridge.DB_Communication()

    def test_bridge(self):
        self.con.insert_to('text')

if __name__ == '__main__':
    unittest.main()
