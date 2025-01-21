from abc import ABC, abstractmethod

class IMonitor(ABC):
    """
    It is entity of monitoring
    """
    @abstractmethod
    def monitor(cls, message, pltype):
        pass