import logging
import random
from Core_layer.Answer_package.Interfaces import IAnswer
from Deep_layer.DB_package.Classes import DB_Communication

class RandomAnswer(IAnswer.IAnswer):
    """

    Summary

    """
    @classmethod
    def answer(cls, text):
#
#
        try:
            inpt = DB_Communication.DB_Communication.get_data(str('SELECT text FROM answer_sets.' + text))
            out = inpt['text'][random.randint(0, (len(inpt)-1))]
            logging.info('The randomanswer.answer is done')
            return str(out)
        except Exception as e:
            logging.exception(str('The exception in randomanswer.answer ' + str(e)))