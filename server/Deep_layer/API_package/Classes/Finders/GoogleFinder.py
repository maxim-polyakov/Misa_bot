import logging
import wikipedia as w
from googlesearch import search
from Deep_layer.API_package.Interfaces import IFinder
import random
import requests
import time

class GoogleFinder(IFinder.IFinder):
    """
    It is the google finder class
    """

    @classmethod
    def find(cls, message_text):
        try:
            output = []

            # Список User-Agents для ротации
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            ]

            # Настройка сессии с прокси (если нужно)
            session = requests.Session()
            session.headers.update({'User-Agent': random.choice(user_agents)})

            time.sleep(random.uniform(3, 7))

            outlist = search(
                message_text,
                num_results=5,
                lang='ru',
                timeout=15,
                sleep_interval=random.uniform(10, 15),  # Большие задержки
                user_agent=random.choice(user_agents)
            )

            for result in outlist:
                output.append(result)

            return set(output)

        except Exception as e:
            logging.exception(f'Error: {e}')
            return set()
