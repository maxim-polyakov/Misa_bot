from abc import ABC, abstractmethod


class IDalle(ABC):
    """
    It is entity of gpt
    """
    @abstractmethod
    def generate(self):
        pass