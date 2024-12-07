from abc import ABC, abstractmethod


class IGpt(ABC):
    """
    It is entyti of gpt
    """
    @abstractmethod
    def generate(self):
        pass