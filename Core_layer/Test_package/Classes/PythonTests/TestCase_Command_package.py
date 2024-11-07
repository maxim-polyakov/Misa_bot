import unittest
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Classes.Commands import CommandAnalyzer
from Core_layer.Test_package.Interfases import ITestCase


class TestCase_API_package(ITestCase.ITestCase):
    """

    This class is written for testing entityes of system

    """
    def test_commandaction(self):
        ac = CommandAction.CommandAction(message='находить нож', message_text='находить нож')
        res = ac.find('bing')
        self.assertNotEqual(res, None)

    def test_commandanalyzerf(self):
        command = CommandAnalyzer.CommandAnalyzer(
            'найди пистолет', 'test')
        output = command.analyse(message_text='найди пистолет')
        self.assertNotEqual(output, None)

    def test_commandanalyzers(self):
        command = CommandAnalyzer.CommandAnalyzer(
            'найди в википедии нож', 'test')
        output = command.analyse(message_text='найди в википедии нож')
        self.assertNotEqual(output, None)

    def test_commandanalyzert(self):
        command = CommandAnalyzer.CommandAnalyzer(
            'найди производную x^2 по x', 'test')
        output = command.analyse(message_text='найди производную x^2 по x')
        self.assertNotEqual(output, None)

    def test_commandanalyzerfi(self):
        command = CommandAnalyzer.CommandAnalyzer(
            'скажи пистолет', 'test')
        output = command.analyse(message_text='скажи пистолет')
        self.assertEqual(output, 'пистолет')

    def test_commandanalyzersi(self):
        command = CommandAnalyzer.CommandAnalyzer(
            'поздоровайся', 'test')
        output = command.analyse(message_text='поздоровайся')
        self.assertNotEqual(output, None)

    def test_commandanalyzerse(self):
        command = CommandAnalyzer.CommandAnalyzer(
            'почисти ввали', 'test')
        output = command.analyse(message_text='почисти ввали')
        self.assertNotEqual(output, None)

if __name__ == '__main__':
    unittest.main()
