from Deep_layer.DB_package.DB_Bridge import DB_Communication
import random
from Core_layer.Answer_package.Answers.Interfaces import IAnswer


class RandomAnswer(IAnswer.IAnswer):


    @classmethod
    def answer(cls):
#
#


            inpt = DB_Communication.DB_Communication.get_data('SELECT * FROM answer_sets.hianswer')
            df = []
            for i in range(0, len(inpt['text']) - 1):
                    df.append(inpt['text'][i])
            number = random.randint(0, len(df))
            return df[number]
