import wikipedia as w
import logging
from Deep_layer.API_package.Interfaces import IFinder


class WikiFinder(IFinder.IFinder):
    """
    it is wiki finder class
    """
    @classmethod
    def find(cls, inptmes):
        # finding something in wikipedia
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # set wikipedia language to russian
            w.set_lang('ru')
            # create a list to store the search result
            return_list = []
            # get the summary of the input term from wikipedia
            return_list.append(w.summary(inptmes))
            # log successful completion of the search
            logging.info('The wikifinder is done')
            # return the first (and only) element of the list
            return return_list[0]
        except Exception as e:
            # log the exception with details
            logging.exception(str('The exception is in wikifinder.find ' + str(e)))
