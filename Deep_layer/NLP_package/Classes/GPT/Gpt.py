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
            client = OpenAI(
                api_key=OPENAI_API_KEY,
                organization=OPENAI_API_ORG,
                project=OPENAI_API_PROJECT,
            )
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{
                    "role": "user",
                    "content": text,
                }],
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].message.content

        except Exception as e:
            logging.exception(str('The exception is in gpt.generate ' + str(e)))
