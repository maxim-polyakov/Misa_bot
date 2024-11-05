from abc import ABC, abstractmethod


class ICalculator(ABC):
    """

    """
    @abstractmethod
    def deravative(cls, boto, message, inptmes, dx):
        pass

    @abstractmethod
    def integrate(cls, boto, message, inptmes, dx):
        pass