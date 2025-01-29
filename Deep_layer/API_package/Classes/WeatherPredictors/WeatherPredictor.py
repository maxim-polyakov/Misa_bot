import requests
import logging
from Deep_layer.API_package.Interfaces import IWeather
from Core_layer.Bot_package.Classes.Token import Token


class WetherPredictor(IWeather.IWeather):
    """
    It is weather prediction class
    """
    city = None

    def __init__(self, city):
        WetherPredictor.city = city

    @classmethod
    def predict(cls):
#
#       Its a method for weather prediction
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            tkn = Token.Token()
            df = tkn.get_token(
                'select token from assistant_sets.tokens where botname = \'Weather\' and platformname = \'Weather\'')
            api = df['token'][0]
            url = 'https://api.openweathermap.org/data/2.5/weather?q=' + cls.city + '&units=metric&lang=ru&appid=' + api
            # отправляем запрос на сервер и сразу получаем результат
            weather_data = requests.get(url).json()
            # получаем данные о температуре и о том, как она ощущается
            if weather_data != None:
                if 'city not found' not in weather_data.values():
                    temperature = round(weather_data['main']['temp'])
                    temperature_feels = round(weather_data['main']['feels_like'])

                    out = []
                    foutstr = 'Сейчас в городе ' + cls.city + ' ' + str(temperature) + ' °C'
                    soutstr = 'Ощущается как ' + str(temperature_feels) + ' °C'

                    out.append(foutstr)
                    out.append(soutstr)
                    logging.info('The wetherpredictor.predict is done')
                    return out
        except Exception as e:
            logging.exception(str('The exception is in wetherpredictor.predict' + str(e)))
