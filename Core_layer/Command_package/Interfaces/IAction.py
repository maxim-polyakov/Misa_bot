from abc import ABC, abstractmethod


class IAction(ABC):
    """

    """
    @abstractmethod
    def fas(cls):
        pass
    @abstractmethod
    def find(cls):
        pass
    @abstractmethod
    def translate(cls):
        pass