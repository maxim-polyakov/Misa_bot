from abc import ABC, abstractmethod

class ICommandAction(ABC):

    @abstractmethod
    def fas(cls):
        pass
    @abstractmethod
    def find(cls):
        pass
    @abstractmethod
    def translate(cls):
        pass