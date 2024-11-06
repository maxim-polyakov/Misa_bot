from abc import ABC, abstractmethod

class IMonitor(ABC):
    """
    It is entyti of monitoring
    """
    @abstractmethod
    def monitor(cls, message, pltype):
        pass