from abc import ABC, abstractmethod


class IFinder(ABC):
    """
    It is entyti of finder
    """
    @abstractmethod
    def find(cls):
        pass