from abc import ABC, abstractmethod

class IPreprocessing(ABC):
    """
    Its is entity of preprocessing of textes
    """
    @abstractmethod
    def preprocess_text(self, text):
        pass
    @abstractmethod
    def reversepreprocess_text(self, text):
        pass