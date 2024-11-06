from abc import ABC, abstractmethod

class ITranslator(ABC):
    """
    It is entyti of translator
    """
    @abstractmethod
    def translate(self):
        pass