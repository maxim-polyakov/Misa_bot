from abc import ABC, abstractmethod

class ITranslator(ABC):
    """
    It is entity of translator
    """
    @abstractmethod
    def translate(self):
        pass