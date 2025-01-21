import unittest
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Classes.Commands import CommandAnalyzer
from Core_layer.Test_package.Interfases import ITestCase


class TestCase_Command_package(ITestCase.ITestCase):
    """

    This class is written for testing entityes of system

    """
    def test_commandanalyzerf(self):
        command = CommandAnalyzer.CommandAnalyzer(
            'найди пистолет', 'test')
        output = command.analyse(message_text='найди пистолет')
        self.assertNotEqual(output, None)

    def test_commandanalyzers(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'найди в википедии нож', 'test')
        output = command.analyse(message_text='найди в википедии нож')
        self.assertNotEqual(output, None)

    def test_commandanalyzert(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'найди производную x^2 по x', 'test')
        output = command.analyse(message_text='найди производную x^2 по x')
        self.assertNotEqual(output, None)

    def test_commandanalyzerfi(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'скажи пистолет', 'test')
        output = command.analyse(message_text='скажи пистолет')
        self.assertNotEqual(output, None)

    def test_commandanalyzersi(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'поздоровайся', 'test')
        output = command.analyse(message_text='поздоровайся')
        self.assertNotEqual(output, None)

    def test_commandanalyzerse(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'почисти ввали', 'test')
        output = command.analyse(message_text='почисти ввали')
        self.assertNotEqual(output, None)

    def test_commandanalyzerei(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'аплодировать', 'test')
        output = command.analyse(message_text='аплодировать')
        self.assertNotEqual(output, None)

    def test_commandanalyzerni(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'поссчитай производную x^2 по x', 'test')
        output = command.analyse(message_text='поссчитай производную x^2 по x')
        self.assertNotEqual(output, None)

    def test_commandanalyzerte(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'абонируй васю', 'test')
        output = command.analyse(message_text='абонируй васю')
        self.assertNotEqual(output, None)

    def test_commandanalyzerel(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'переведи knife', 'test')
        output = command.analyse(message_text='переведи knife')
        self.assertNotEqual(output, None)

    def test_commandanalyzertw(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'абонируйся', 'test')
        output = command.analyse(message_text='абонируйся')
        self.assertNotEqual(output, None)

    def test_commandanalyzerthi(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'абсолютизируй', 'test')
        output = command.analyse(message_text='абсолютизируй')
        self.assertNotEqual(output, None)

    def test_commandanalyzerfour(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'абсолютизируйся', 'test')
        output = command.analyse(message_text='абсолютизируйся')
        self.assertNotEqual(output, None)

    def test_commandanalyzerfif(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'абсолютируй', 'test')
        output = command.analyse(message_text='абсолютируй')
        self.assertNotEqual(output, None)

    def test_commandanalyzersix(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'абсорбируйся', 'test')
        output = command.analyse(message_text='абсорбируйся')
        self.assertNotEqual(output, None)

    def test_commandanalyzerseven(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'абстрагируй', 'test')
        output = command.analyse(message_text='абстрагируй')
        self.assertNotEqual(output, None)

    def test_commandanalyzereight(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'автоматизируйся', 'test')
        output = command.analyse(message_text='автоматизируйся')
        self.assertNotEqual(output, None)

    def test_commandanalyzernine(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'погода', 'test')
        output = command.analyse(message_text='погода')
        self.assertNotEqual(output, None)

    def test_commandanalyzertwntn(self):
        command = CommandAnalyzer.CommandAnalyzer('boto',
            'нарисуй кота', 'test')
        output = command.analyse(message_text='нарисуй кота')
        self.assertNotEqual(output, None)

if __name__ == '__main__':
    unittest.main()
