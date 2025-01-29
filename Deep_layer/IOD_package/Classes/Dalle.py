from Deep_layer.NLP_package.Interfaces import IGpt
from openai import OpenAI
import logging
from Deep_layer.DB_package.Classes import DB_Communication
from Deep_layer.NLP_package.Classes.TextPreprocessers import QuestionPreprocessing

class Dalle(IGpt.IGpt):
    """
    It is a dalle image generator
    """
    __dbc = DB_Communication.DB_Communication()
    __pr = QuestionPreprocessing.QuestionPreprocessing()

    @classmethod
    def generate(cls, text):
#
#       Its a method for generating url with pictures
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            fdf = cls.__dbc.get_data('select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Gpt\'')
            sdf = cls.__dbc.get_data('select token from assistant_sets.projects where botname = \'Misa\' and platformname = \'Gpt\'')
            tdf = cls.__dbc.get_data('select token from assistant_sets.organizations where botname = \'Misa\' and platformname = \'Gpt\'')
            OPENAI_API_KEY = fdf['token'][0]
            OPENAI_API_PROJECT = sdf['token'][0]
            OPENAI_API_ORG = tdf['token'][0]
            client = OpenAI(
                api_key=OPENAI_API_KEY,
                organization=OPENAI_API_ORG,
                project=OPENAI_API_PROJECT,
            )
            input_text = cls.__pr.preprocess_text(text)
            response = client.images.generate(
                model="dall-e-3",
                prompt=input_text,
                size="1024x1024",
                n=1,
            )
            image_url = response.data[0].url
            return str(image_url)

        except Exception as e:
            logging.exception(str('The exception is in dalle.generate ' + str(e)))
