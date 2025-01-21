import logging
from Deep_layer.API_package.Classes.Finders import GoogleFinder
from Core_layer.Bot_package.Interfaces import IFinder


class GoogleFinder(IFinder.IFinder):
    """

    That's a class drawer. It describes an image drawing algorithm.

    """
    message_text = None
    __gfind = GoogleFinder.GoogleFinder()
    def __init__(self, message_text):
        GoogleFinder.message_text = message_text
    @classmethod
    def find(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            gpif = GoogleFinder.GoogleFinder()
            finded_list = gpif.find(cls.message_text)
            outstr = 'Ссылки по запросу:\n'
            if (finded_list != None):
                for outmes in finded_list:
                    outstr += outmes + ' \n '
            logging.info('The googlefinder.find is done')
            if outstr == '':
                return 'Не нашла'
            return outstr

        except Exception as e:
            logging.exception(str('The exception in googlefinder.find ' + str(e)))
