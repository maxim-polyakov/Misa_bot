from Deep_layer.NLP_package.Interfaces import IGpt
from openai import OpenAI
import logging
from Deep_layer.DB_package.Classes import DB_Communication
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing

class Dalle(IGpt.IGpt):
    """
    It is a gpt text generator
    """
    __dbc = DB_Communication.DB_Communication()
    @classmethod
    def generate(cls, text):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            fdf = cls.__dbc.get_data('select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Gpt\'')
            sdf = cls.__dbc.get_data('select token from assistant_sets.projects where botname = \'Misa\' and platformname = \'Gpt\'')
            tdf = cls.__dbc.get_data('select token from assistant_sets.organizations where botname = \'Misa\' and platformname = \'Gpt\'')
            OPENAI_API_KEY = fdf['token'][0]
            OPENAI_API_PROJECT = sdf['token'][0]
            OPENAI_API_ORG = tdf['token'][0]

        except Exception as e:
            logging.exception(str('The exception is in gpt.generate ' + str(e)))
