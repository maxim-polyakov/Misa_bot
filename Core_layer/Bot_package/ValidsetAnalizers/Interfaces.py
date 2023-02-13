from abc import ABC, abstractmethod

class IAnalizer(ABC):

    @abstractmethod
    def analize(self):
        pass