from abc import ABC, abstractmethod

class ICleaner(ABC):
    """
    It is entyti of cleaning
    """
    @abstractmethod
    def clean(cls):
        pass