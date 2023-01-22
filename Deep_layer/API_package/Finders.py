import wikipedia as w
from abc import ABC, abstractmethod

class IFinder(ABC):

    @abstractmethod
    def find(cls):
        pass

class WikiFinder(IFinder):

    @classmethod
    def find(cls,inptmes):
        try:
            w.set_lang('ru')
            return_list = []
            return_list.append(w.summary(inptmes))

            return return_list[0]
        except:
            return return_list[0]