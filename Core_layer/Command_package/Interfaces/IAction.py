from abc import ABC, abstractmethod


class IAction(ABC):
    """
    It is entyti of action
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