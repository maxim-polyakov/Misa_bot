from abc import ABC, abstractmethod


class ICalculator(ABC):
    """
    It is entity of calculator
    """
    @abstractmethod
    def deravative(cls, boto, message, inptmes, dx):
        pass

    @abstractmethod
    def integrate(cls, boto, message, inptmes, dx):
        pass