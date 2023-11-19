from abc import ABC, abstractmethod


class IModel(ABC):


    """

    This entity is for Modeling

    """

    @abstractmethod
    def train(self, target):
        pass

    @abstractmethod
    def train(self, target, epochs):
        pass
