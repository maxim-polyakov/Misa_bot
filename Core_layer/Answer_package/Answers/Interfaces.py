from abc import ABC, abstractmethod

class IAnswer(ABC):

    @abstractmethod
    def answer(self):
        pass