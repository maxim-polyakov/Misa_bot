from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IWeather
import requests

class MemoryCleaner(IWeather.IWeather):

    @classmethod
    def predict(cls, city):
        pass