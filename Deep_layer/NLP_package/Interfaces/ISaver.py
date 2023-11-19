from abc import ABC, abstractmethod

class ISaver(ABC):


    """

    This entyty is for a saving any results i na picture

    """
    @abstractmethod
    def saveRes(cls, history, path, accuracy):
        pass