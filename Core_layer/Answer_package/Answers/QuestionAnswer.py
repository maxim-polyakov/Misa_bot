from Deep_layer.NLP_package.GPT import Gpt
import re
from Core_layer.Answer_package.Answers import IAnswer

class QuestionAnswer(IAnswer.IAnswer):
    __gpt = Gpt.Gpt

    @classmethod
    def answer(self, text):
        generated_text = self.__gpt.generate("Вопрос: '" + text + "\'")
        text = re.sub('  ', ' ', generated_text.replace('Ответ', '').replace('Вопрос', '').replace(text, '')
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
        if( not tokens[0]):
            tokens[0] = "Не знаю."

        text = str(tokens[0]) + str(symbbuff)
        return text