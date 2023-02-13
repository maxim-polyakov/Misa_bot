from abc import ABC, abstractmethod

class IAnalizer(ABC):

    @abstractmethod
    def analyze(self):
        pass