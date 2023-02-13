from abc import ABC, abstractmethod

class IToken(ABC):

    @abstractmethod
    def add_token(cls, token):
        pass

    @abstractmethod
    def get_token(cls, select):
        pass