from abc import ABC, abstractmethod

class ISaver(ABC):

    @abstractmethod
    def saveRes(cls, history, path):
        pass