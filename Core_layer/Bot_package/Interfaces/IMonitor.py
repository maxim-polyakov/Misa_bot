from abc import ABC, abstractmethod

class IMonitor(ABC):

    @abstractmethod
    def monitor(cls, message, command, pltype):
        pass