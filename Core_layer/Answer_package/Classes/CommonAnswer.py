from Deep_layer.NLP_package.Classes.GPT import Gpt
import re
from Core_layer.Answer_package.Interfaces import IAnswer


class CommonAnswer(IAnswer.IAnswer):
    """

    Summary

    """
    __gpt = Gpt.Gpt

    @classmethod
    def answer(self, text):
        generated_text = self.__gpt.generate("Вопрос: '" + text + "\'")
        text = re.sub('  ', ' ',
                      generated_text.replace('Ответ', '').replace('Вопрос', '').replace(text, '').replace(':', '')
                      .replace('\'', '').lstrip(' '))
        return str(text)