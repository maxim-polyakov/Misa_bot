from abc import ABC, abstractmethod

class IAnalyzer(ABC):

    @abstractmethod
    def analyze(self):
        pass