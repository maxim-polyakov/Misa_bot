from abc import ABC, abstractmethod


class IAnswer(ABC):
    """
    Its entity of answering
    """
    @abstractmethod
    def answer(self):
        pass