from Deep_layer.DB_package.Classes import DB_Communication as bridge
from Core_layer.Test_package.Interfases import ITestCase
import unittest

class TestCase_DB_package(ITestCase.ITestCase):


    """

    This class is written for testing an entityes of system

    """
    con = bridge.DB_Communication()

    def test_bridge(self):
        data = self.con.get_data('SELECT * FROM assistant_sets.test_table')
        self.con.insert_to(data, 'test_table')
        self.assertNotEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()
