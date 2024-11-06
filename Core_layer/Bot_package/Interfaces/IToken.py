from abc import ABC, abstractmethod

class IToken(ABC):
    """
    It is entyti of tokens
    """
    @abstractmethod
    def add_token(cls, token):
        pass

    @abstractmethod
    def get_token(cls, select):
        pass