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
#       Finding something in google
#       Configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
#           List to store search results
            output = []
#           Performing a google search with specified parameters
            outlist = search(message_text, tld="co.in", num=9, stop=9, pause=1)
#           Collecting search results
            for result in outlist:
                output.append(result)
#           Logging successful completion of the search
            logging.info('The googlefinder.find is done')
#           Returning unique search results as a set
            return set(output)
        except Exception as e:
#           Logging the exception with details
            logging.exception(str('The exception is in googlefinder.find ' + str(e)))
