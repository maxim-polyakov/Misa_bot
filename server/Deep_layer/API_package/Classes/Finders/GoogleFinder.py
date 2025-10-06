import logging
import wikipedia as w
from googlesearch import search
from Deep_layer.API_package.Interfaces import IFinder


class GoogleFinder(IFinder.IFinder):
    """
    It is the google finder class
    """
    @classmethod
    def find(cls, message_text):
        # finding something in google
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # list to store search results
            output = []
            # performing a google search with specified parameters
            outlist = search(
                message_text,
                num=9,
                stop=9,
                pause=2,  # Увеличиваем паузу
                tld='co.in'  # Домен (можно попробовать 'co.in' и др.)
            )
            # collecting search results
            for result in outlist:
                output.append(result)
            # logging successful completion of the search
            logging.info('The googlefinder.find method has completed successfully')
            # returning unique search results as a set
            return set(output)
        except Exception as e:
            # logging the exception with details
            logging.exception('The exception occurred in googlefinder.find: ' + str(e))
