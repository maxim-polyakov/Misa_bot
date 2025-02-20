import logging
from Deep_layer.API_package.Classes.Finders import WikiFinder as wfinder
from Core_layer.Bot_package.Interfaces import IFinder


class WikiFinder(IFinder.IFinder):
    """

    That's a class drawer. It describes an image drawing algorithm.

    """
    message_text = None
    def __init__(self, message_text):
        WikiFinder.message_text = message_text
    @classmethod
    def find(cls):
        # finding by google funder
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # log that the search operation was completed successfully
            logging.info('The wikifinder.find process has completed successfully')
        except Exception as e:
            # log any exceptions that occur during the search process
            logging.exception('The exception occurred in wikifinder.find: ' + str(e))
