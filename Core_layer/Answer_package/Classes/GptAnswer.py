import re
import logging
from Core_layer.Answer_package.Interfaces import IAnswer
from Deep_layer.NLP_package.Classes.GPT import Gpt


class GptAnswer(IAnswer.IAnswer):
    """

    It is class for question answering

    """
    __gpt = Gpt.Gpt()

    @classmethod
    def answer(cls, text):

        try:
            generated_text = cls.__gpt.generate(text)
            logging.info('The gptanswer.answer is done')
            return generated_text
        except Exception as e:
            logging.exception(str('The exception in questionanswer.answer ' + str(e)))