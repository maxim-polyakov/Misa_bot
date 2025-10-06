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

    import requests
    import time
    import random
    import logging
    from googlesearch import search

    @classmethod
    def find(cls, message_text):
        try:
            output = []

            # Случайная задержка
            time.sleep(random.uniform(5, 10))

            # Кастомные заголовки
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            ]

            outlist = search(
                message_text,
                num_results=3,  # Уменьшаем до 3
                lang='ru',
                timeout=20,
                # Библиотека автоматически использует случайные User-Agent
            )

            for result in outlist:
                output.append(result)
                # Задержка между получением результатов
                time.sleep(random.uniform(2, 4))

            return set(output)

        except Exception as e:
            logging.exception(f'Error: {e}')
            return set()
