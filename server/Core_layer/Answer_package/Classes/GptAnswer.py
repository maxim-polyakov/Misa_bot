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
    def answer(cls, text, is_command_check):
        # generating answers by gpt
        # configure logging to write logs to a file
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # generate an answer using the gpt model
            generated_text = cls.__gpt.generate(text, is_command_check)
            # log successful completion of the answer generation
            logging.info('The gptanswer.answer process has completed successfully')
            return generated_text
        except Exception as e:
            # log the exception if an error occurs during answer generation
            logging.exception('The exception occurred in questionanswer.answer: ' + str(e))
