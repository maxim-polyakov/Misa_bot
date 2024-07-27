from Deep_layer.DB_package.Classes import DB_Communication
import random
from Core_layer.Answer_package.Interfaces import IAnswer


class RandomAnswer(IAnswer.IAnswer):
    """

    Summary

    """


    @classmethod
    def answer(cls, text):
#
#
        inpt = DB_Communication.DB_Communication.get_data(str('SELECT text FROM answer_sets.' + text))
        out = inpt['text'][random.randint(0, (len(inpt)-1))]
        return str(out)
