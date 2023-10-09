from abc import ABC, abstractmethod


class IModel(ABC):


    @abstractmethod
    def train(self, target):
        pass
