from abc import ABC, abstractmethod


class IAnalyzer(ABC):

    @abstractmethod
    def analyse(self, message_text):
        pass