from abc import ABC, abstractmethod

class ICleaner(ABC):
    """
    It is entity of cleaning
    """
    @abstractmethod
    def clean(cls):
        pass