from abc import ABC, abstractmethod

class ITokenizer(ABC):


    """

    This entyty is for a tokenization any textes of data frames

    """

    @abstractmethod
    def train_tokenize(self):
        pass

    @abstractmethod
    def vectorize_input(self):
        pass