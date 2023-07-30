from abc import ABC, abstractmethod

class ITestMonitor(ABC):

    @abstractmethod
    def monitor(self):
        pass