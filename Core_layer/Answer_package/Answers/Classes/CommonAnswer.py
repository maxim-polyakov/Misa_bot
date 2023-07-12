from Deep_layer.NLP_package.GPT import Gpt
import re
from Core_layer.Answer_package.Answers.Interfaces import IAnswer


class CommonAnswer(IAnswer.IAnswer):
    __gpt = Gpt.Gpt

    @classmethod
    def answer(self, text):
        generated_text = self.__gpt.generate("Вопрос: '" + text + "\'")
        text = re.sub('  ', ' ',
                      generated_text.replace('Ответ', '').replace('Вопрос', '').replace(text, '').replace(':', '')
                      .replace('\'', '').lstrip(' '))
        return str(text)