from abc import ABC, abstractmethod

class IFinder(ABC):

    @abstractmethod
    def find(cls):
        pass