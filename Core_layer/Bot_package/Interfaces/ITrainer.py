from abc import ABC, abstractmethod

class ITrainer(ABC):

    @abstractmethod
    def hitrain(cls):
        pass
    @abstractmethod
    def thtrain(cls):
        pass
    @abstractmethod
    def businesstrain(cls):
        pass
    @abstractmethod
    def weathertrain(cls):
        pass
    @abstractmethod
    def emotionstrain(cls):
        pass
    @abstractmethod
    def trashtrain(cls):
        pass