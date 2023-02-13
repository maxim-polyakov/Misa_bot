from Deep_layer.DB_package import DB_Bridge
from Deep_layer.NLP_package import GPT
import random
import re
from Core_layer.Answer_package.Answers import Interfaces

class RandomAnswer(Interfaces.IAnswer):
    __inpt = DB_Bridge.DB_Communication.get_data('SELECT * FROM answer_sets.hianswer')
    __data = __inpt
    __df = []

    @classmethod
    def answer(self):
        try:
            for i in range(0, len(self.__data['text']) - 1):
                if (self.__data['agenda'][i] == 'Приветствие'):
                    self.__df.append(self.__data['text'][i])
            outmapa = {0: [self.__df[random.randint(0, len(self.__df))]]}

            return (outmapa[0])
        except:
            return 'The exception in RandomAnswer.answer'


class QuestionAnswer(Interfaces.IAnswer):
    __gpt = GPT.Gpt

    @classmethod
    def answer(self, text):
        generated_text = self.__gpt.generate("Вопрос: '" + text + "\'")
        text = re.sub('  ', ' ', generated_text.replace('Ответ', '').replace('Вопрос', '').replace(text, '')
                      .replace(':', '').replace('\'', '').lstrip(' '))
        return text


class CommonAnswer(Interfaces.IAnswer):
    __gpt = GPT.Gpt

    @classmethod
    def answer(self, text):
        generated_text = self.__gpt.generate("Вопрос: '" + text + "\'")
        text = re.sub('  ', ' ',
                      generated_text.replace('Ответ', '').replace('Вопрос', '').replace(text, '').replace(':', '')
                      .replace('\'', '').lstrip(' '))
        return text