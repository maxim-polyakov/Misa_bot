from abc import ABC, abstractmethod

class IWeather(ABC):
    """
    It is entyti of weather service
    """
    @abstractmethod
    def predict(cls):
        pass