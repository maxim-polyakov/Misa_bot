import logging
import wikipedia as w
from googlesearch import search
from Deep_layer.API_package.Interfaces import IFinder


class GoogleFinder(IFinder.IFinder):
    """
    It is google finder class
    """
    @classmethod
    def find(cls, message_text):

        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            output = []
            outlist = search(message_text, num_results=9, advanced=True, region="ru", lang="ru")

            for outex in outlist:
                output.append(str(outex.title) + ' ' + str(outex.url))
            logging.info('The googlefinder.find is done')
            if output == []:
                return "Не нашла"
            return set(output)
        except Exception as e:
            logging.exception(str('The exception is in googlefinder.find ' + str(e)))
