import wikipedia as w
from Deep_layer.API_package.Finders import IFinder

class WikiFinder(IFinder.IFinder):

    @classmethod
    def find(cls, inptmes):


        try:
            w.set_lang('ru')
            return_list = []
            return_list.append(w.summary(inptmes))
            return return_list[0]
        except:
            return return_list[0]
