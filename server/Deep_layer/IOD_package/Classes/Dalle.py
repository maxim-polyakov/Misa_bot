from Deep_layer.NLP_package.Interfaces import IGpt
from openai import OpenAI
import base64
import logging
from Deep_layer.DB_package.Classes import DB_Communication
from Deep_layer.NLP_package.Classes.TextPreprocessers import QuestionPreprocessing

class Dalle(IGpt.IGpt):
    """
    Генератор изображений через OpenAI gpt-image-2.
    """
    __dbc = DB_Communication.DB_Communication()
    __pr = QuestionPreprocessing.QuestionPreprocessing()

    @classmethod
    def generate(cls, text):
        # generating url with pictures
        # configuring logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # retrieving api tokens from the database
            fdf = cls.__dbc.get_data('select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Gpt\'')
            sdf = cls.__dbc.get_data('select token from assistant_sets.projects where botname = \'Misa\' and platformname = \'Gpt\'')
            tdf = cls.__dbc.get_data('select token from assistant_sets.organizations where botname = \'Misa\' and platformname = \'Gpt\'')
            # extracting api keys from the retrieved data
            OPENAI_API_KEY = fdf['token'][0]
            OPENAI_API_PROJECT = sdf['token'][0]
            OPENAI_API_ORG = tdf['token'][0]
            # initializing openai client with api credentials
            client = OpenAI(
                api_key=OPENAI_API_KEY,
                organization=OPENAI_API_ORG,
                project=OPENAI_API_PROJECT,
            )
            # preprocessing the input text
            input_text = cls.__pr.preprocess_text(text)
            response = client.images.generate(
                model="gpt-image-2",
                prompt=input_text,
                size="1024x1024",
                n=1,
            )
            b64_data = response.data[0].b64_json
            if not b64_data:
                raise ValueError('gpt-image-2 returned no image data')
            image_bytes = base64.b64decode(b64_data)
            logging.info('The dalle.generate method has completed successfully')
            return image_bytes
        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception('The exception occurred in dalle.generate: ' + str(e))
