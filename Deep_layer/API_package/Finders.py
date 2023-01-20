from Deep_layer import API_package


class IFinder(API_package.ABC):

    @API_package.abstractmethod
    def find(cls):
        pass
    
    
class WikiFinder(IFinder):

    @classmethod
    def find(cls,inptmes):
        try:
            API_package.w.set_lang('ru')
            return_list = []
            return_list.append(API_package.w.summary(inptmes))

            return return_list[0]
        except:
            return return_list[0]