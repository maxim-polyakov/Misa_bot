import wikipedia as w
import logging
from Deep_layer.API_package.Interfaces import IFinder


class WikiFinder(IFinder.IFinder):
    """
    it is wiki finder class
    """
    @classmethod
    def find(cls, inptmes):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            w.set_lang('ru')
            return_list = []
            return_list.append(w.summary(inptmes))
            logging.info('The wikifinder is done')
            return return_list[0]
        except Exception as e:
            logging.exception(str('The exception is in wikifinder.find ' + str(e)))
