from abc import ABC, abstractmethod

class IMonitor(ABC):

    @abstractmethod
    def monitor(self):
        pass