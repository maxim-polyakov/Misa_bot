import requests
import logging
import wikipedia as w
from bs4 import BeautifulSoup
from Deep_layer.API_package.Interfaces import IFinder


class BingFinder(IFinder.IFinder):
    """
    It is the bing finder class
    """
    @classmethod
    def find(cls, message_text):
#
#       Its method for finding simething in bing
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            url = f"https://www.bing.com/search?q={message_text}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('li', class_='b_algo')
            output = []

            for counter, result in enumerate(results):
                title = result.find('h2').text
                link = result.find('a')['href']
                output.append(str(counter) + ' ' + str(title) + ' ' + str(link))

            logging.info('The bingfinder.find is done')
            return output
        except Exception as e:
            logging.exception(str('The exception is in bingfinder.find ' + str(e)))
