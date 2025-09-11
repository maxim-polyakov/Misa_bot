from abc import ABC, abstractmethod

class IFinder:
    """
    It is entity of finding
    """
    @abstractmethod
    def find(self):
        pass