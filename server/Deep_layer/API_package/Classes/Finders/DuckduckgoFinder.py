import logging
import wikipedia as w
from duckduckgo_search import DDGS
from Deep_layer.API_package.Interfaces import IFinder
import random
import time

class DuckduckgoFinder(IFinder.IFinder):
    """
    It is the google finder class
    """

    @classmethod
    def find(cls, message_text):
        try:
            # Задержка
            time.sleep(random.uniform(2, 5))

            output = []
            ddgs = DDGS()

            results = ddgs.text(
                keywords=message_text,
                region='ru-ru',
                max_results=5
            )

            for result in results:
                output.append(result['href'])

            return set(output)

        except Exception as e:
            logging.exception(f'Error: {e}')
            return set()