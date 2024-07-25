from Deep_layer.DB_package.Classes import DB_Communication
import random
from Core_layer.Answer_package.Interfaces import IAnswer


class RandomAnswer(IAnswer.IAnswer):
    """

    Summary

    """
    __inpt = DB_Communication.DB_Communication.get_data('SELECT * FROM answer_sets.hianswer')
    __data = __inpt
    __df = []

    @classmethod
    def answer(self, text):
#
#
        if text ==0:
            for i in range(0, len(self.__data['text']) - 1):
                self.__df.append(self.__data['text'][i])
            outmapa = {0: self.__df[random.randint(0, len(self.__df))]}
            return str(outmapa[0])
        return 'Привет'