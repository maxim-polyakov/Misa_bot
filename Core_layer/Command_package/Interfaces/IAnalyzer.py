from abc import ABC, abstractmethod


class IAnalyzer(ABC):
    """
    It is entyti of analyzing
    """
    @abstractmethod
    def analyse(self, message_text):
        pass