import logging
from Deep_layer.API_package.Classes.Finders import GoogleFinder as gfinder
from Core_layer.Bot_package.Interfaces import IFinder


class GoogleFinder(IFinder.IFinder):
    """

    That's a class drawer. It describes an image drawing algorithm.

    """
    message_text = None

    def __init__(self, message_text):
        GoogleFinder.message_text = message_text

    @classmethod
    def find(cls):
        # finding by google funder
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # create an instance of googlefinder
            gpif = gfinder.GoogleFinder()
            # perform a search using googlefinder
            finded_list = gpif.find(cls.message_text)
            # prepare the output string with proper capitalization
            outstr = 'Ссылки по запросу:\n'
            # check if any results were found
            if finded_list:
                for outmes in finded_list:
                    outstr += outmes + ' \n '
            else:
                return 'Не нашла'

            # log that the search operation was completed successfully
            logging.info('The googlefinder.find process has completed successfully')
            return outstr

        except Exception as e:
            # log any exceptions that occur during the search process
            logging.exception('The exception occurred in googlefinder.find: ' + str(e))
            return 'Произошла ошибка при поиске'