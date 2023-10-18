from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorTelegram
from Core_layer.Test_package.Interfases import ITestCase
import unittest
class TestCase_API_package(ITestCase.ITestCase):
    """

    Summary

    """
    def test_MessageMonitorTelegram(self):
        message = {"message_id": 2953, "from": {"id": 1266526074, "is_bot": False,
                                                "first_name": "Maxim", "last_name": "Polyakov",
                                                "username": "The_Baxic", "language_code": "en"},
                                                "chat": {"id": 1266526074, "first_name": "Maxim",
                                                         "last_name": "Polyakov", "username": "The_Baxic",
                                                         "type": "private"},
                                                "date": 1677968619, "text": "миса покажжи данные по hi"}

        mon = MessageMonitorTelegram.MessageMonitorTelegram(message)
        mon.monitor()



if __name__ == '__main__':
    unittest.main()
