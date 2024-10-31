import wikipedia as w
import logging
from Deep_layer.API_package.Interfaces import IFinder


class WikiFinder(IFinder.IFinder):

    @classmethod
    def find(cls, inptmes):


        try:
            w.set_lang('ru')
            return_list = []
            return_list.append(w.summary(inptmes))
            return return_list[0]
            logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
            logging.info(str(return_list[0]))
        except Exception as e:
            logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
            logging.exception(str('The exception is in WikiFinder.find' + e))