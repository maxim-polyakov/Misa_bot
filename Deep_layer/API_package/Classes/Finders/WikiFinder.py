import wikipedia as w
from Deep_layer.API_package.Interfaces import IFinder


class WikiFinder(IFinder.IFinder):
    """

    Summary

    """
    @classmethod
    def find(cls, inptmes):


        try:
            w.set_lang('ru')
            return_list = []
            return_list.append(w.summary(inptmes))
            return return_list[0]
        except:
            return return_list[0]
