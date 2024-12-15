from abc import ABC, abstractmethod


class IDalle(ABC):
    """
    It is entyti of gpt
    """
    @abstractmethod
    def generate(self):
        pass