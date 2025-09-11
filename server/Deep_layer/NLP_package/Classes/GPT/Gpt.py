from Deep_layer.NLP_package.Interfaces import IGpt
from openai import OpenAI
import logging
from Deep_layer.DB_package.Classes import DB_Communication

class Gpt(IGpt.IGpt):
    """
    It is a gpt text generator
    """
    __dbc = DB_Communication.DB_Communication()
    @classmethod
    def generate(cls, text):
        # generating answers
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
            # sending a request to the gpt model to generate a response
            response = client.chat.completions.create(
                model='chatgpt-4o-latest',
                messages=[{
                    "role": "user",
                    "content": text,
                }],
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            # logging successful completion of the method
            logging.info('The gpt.generate method has completed successfully')
            # returning the generated response
            return response.choices[0].message.content
        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception('The exception occurred in gpt.generate: ' + str(e))
