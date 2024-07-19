from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IWeather
import requests

class WetherPredictor(IWeather.IWeather):

    city = None
    temperature = None
    temperature_feels = None

    def __init__(self, city):
        WetherPredictor.city = city

    @classmethod
    def __get(cls):
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + cls.city + '&units=metric&lang=ru&appid=2133d9a270be8e41515cce9d14a0636d'
        # отправляем запрос на сервер и сразу получаем результат
        weather_data = requests.get(url).json()
        # получаем данные о температуре и о том, как она ощущается
        cls.temperature = round(weather_data['main']['temp'])
        cls.temperature_feels = round(weather_data['main']['feels_like'])

    @classmethod
    def predict(cls):
        try:
            cls.__get()
        except:
            cls.__get()

        out = []
        foutstr = 'Сейчас в городе ' + cls.city + ' ' + str(cls.temperature) + ' °C'
        soutstr = 'Ощущается как' + str(cls.temperature_feels) + ' °C'

        out.append(foutstr)
        out.append(soutstr)
        return out
