import nltk
from abc import ABC, abstractmethod

class IPreprocessing(ABC):

    @abstractmethod
    def preprocess_text(self, text):
        pass
    @abstractmethod
    def reversepreprocess_text(self,text):
        pass