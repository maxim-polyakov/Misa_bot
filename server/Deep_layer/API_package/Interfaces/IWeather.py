from abc import ABC, abstractmethod

class IWeather(ABC):
    """
    It is entity of weather service
    """
    @abstractmethod
    def predict(cls):
        pass