from abc import ABC, abstractmethod

class IWeather(ABC):

    @abstractmethod
    def predict(cls):
        pass