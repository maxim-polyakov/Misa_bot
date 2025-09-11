from abc import ABC, abstractmethod

class IWeather:
    """
    It is entity of weather's predictions1
    """
    @abstractmethod
    def predict(self):
        pass