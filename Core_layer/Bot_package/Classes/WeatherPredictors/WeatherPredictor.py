from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IWeather
from Core_layer.Bot_package.Classes.Token import Token
import requests

class WetherPredictor(IWeather.IWeather):

    city = None

    def __init__(self, city):
        WetherPredictor.city = city

    @classmethod
    def predict(cls):

        tkn = Token.Token()
        df = tkn.get_token(
            'select token from assistant_sets.tokens where botname = \'Weather\' and platformname = \'Weather\'')
        api = df['token'][0]
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + cls.city + '&units=metric&lang=ru&appid=' + api
        # отправляем запрос на сервер и сразу получаем результат
        weather_data = requests.get(url).json()
        # получаем данные о температуре и о том, как она ощущается
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])

        out = []
        foutstr = 'Сейчас в городе ' + cls.city + ' ' + str(temperature) + ' °C'
        soutstr = 'Ощущается как ' + str(temperature_feels) + ' °C'

        out.append(foutstr)
        out.append(soutstr)
        return out
