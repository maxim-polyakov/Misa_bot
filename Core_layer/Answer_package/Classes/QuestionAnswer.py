from Deep_layer.NLP_package.Classes.GPT import Gpt
import re
from Core_layer.Answer_package.Interfaces import IAnswer


class QuestionAnswer(IAnswer.IAnswer):
    """

    Summary

    """
    __gpt = Gpt.Gpt

    @classmethod
    def answer(self, text):
        generated_text = self.__gpt.generate("Вопрос: '" + text + "\'")
        text = re.sub(' ', ' ', generated_text.replace('Ответ', '').replace('Вопрос', '').replace(text, '')
                      .replace(':', '').replace('\'', '').lstrip(' '))

        tokens = text.split(' ')
        symbbuff = ''
        if(text.count('?') > 0):
            tokens = text.split('?')
            symbbuff = '?'
        elif(text.count('.')>0):
            tokens = text.split('.')
            symbbuff = '.'
        elif (text.count('!')>0):
            tokens = text.count('!')
            symbbuff = '!'

        text = str(tokens[0]) + str(symbbuff)
        return text