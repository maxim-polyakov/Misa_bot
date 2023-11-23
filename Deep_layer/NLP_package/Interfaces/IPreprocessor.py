from abc import ABC, abstractmethod

class IPreprocessor(ABC):


    """

    This entyty is for Preprocessing of textes

    """
    @abstractmethod
    def preprocess_text(self, text):
        pass

    @abstractmethod
    def reversepreprocess_text(self, text):
        pass