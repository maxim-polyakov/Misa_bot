from abc import ABC, abstractmethod


class IAnalyzer(ABC):
    """
    It is entity of analyzing
    """
    @abstractmethod
    def analyse(self, message_text):
        pass