from abc import ABC, abstractmethod


class IFinder(ABC):
    """
    It is entity of finder
    """
    @abstractmethod
    def find(cls):
        pass