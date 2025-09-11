from abc import ABC, abstractmethod


class IGpt(ABC):
    """
    It is entity of gpt
    """
    @abstractmethod
    def generate(self):
        pass