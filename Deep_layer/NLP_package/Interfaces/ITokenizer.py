from abc import ABC, abstractmethod

class ITokenizer(ABC):


    @abstractmethod
    def train_tokenize(self):
        pass
    @abstractmethod
    def vectorize_input(self):
        pass