from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IWeather
import requests

class WetherPredictor(IWeather.IWeather):

    city = None

    def __init__(self, city):
        WetherPredictor.city = city
    @classmethod
    def predict(cls):
        url = str('https://api.openweathermap.org/data/2.5/weather?q='+cls.city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347')
        # отправляем запрос на сервер и сразу получаем результат
        weather_data = requests.get(url).json()
        # получаем данные о температуре и о том, как она ощущается
        temperature = round(weather_data['main']['temp'])
        #temperature_feels = round(weather_data['main']['feels_like'])
        # выводим значения на экран,

        out = []
        foutstr = 'Сейчас в городе ' + cls.city + ' ' + str(temperature) + ' °C'
        #soutstr = 'Ощущается как' + str(temperature_feels) + ' °C'

        out.append(foutstr)
        #out.append(soutstr)
        return out
