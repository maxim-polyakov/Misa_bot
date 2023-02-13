from abc import ABC, abstractmethod

class ICommandAnalyzer(ABC):

    @abstractmethod
    def commandanalyse(self, message_text):
        pass