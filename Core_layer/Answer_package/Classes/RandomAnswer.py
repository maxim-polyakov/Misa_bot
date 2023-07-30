from Deep_layer.DB_package.Classes import DB_Communication
import random
from Core_layer.Answer_package.Interfaces import IAnswer


class RandomAnswer(IAnswer.IAnswer):
    __inpt = DB_Communication.DB_Communication.get_data('SELECT * FROM answer_sets.hianswer')
    __data = __inpt
    __df = []

    @classmethod
    def answer(self):
#
#
        try:
            for i in range(0, len(self.__data['text']) - 1):
                if (self.__data['agenda'][i] == 'Приветствие'):
                    self.__df.append(self.__data['text'][i])
            outmapa = {0: [self.__df[random.randint(0, len(self.__df))]]}
            if(outmapa[0] != 'Т'):
                return str(outmapa[0])
            else:
                return 'Привет'
        except:
            return 'The exception in RandomAnswer.answer'