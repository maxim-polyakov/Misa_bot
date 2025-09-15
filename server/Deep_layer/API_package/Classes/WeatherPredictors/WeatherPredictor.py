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
        # weather prediction
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # retrieve api token for weather data
            tkn = Token.Token()
            df = tkn.get_token(
                'select token from assistant_sets.tokens where botname = \'Weather\' and platformname = \'Weather\'')
            api = df['token'][0]
            # construct the api request url
            url = 'https://api.openweathermap.org/data/2.5/weather?q=' + cls.city + '&units=metric&lang=ru&appid=' + api
            # send request to the weather api and get the response in json format
            response = requests.get(url, timeout=10).json()
            weather_data = response.json()
            # check if the response contains valid weather data
            if weather_data != None:
                if 'city not found' not in weather_data.values():
                    # extract temperature and "feels like" temperature
                    temperature = round(weather_data['main']['temp'])
                    temperature_feels = round(weather_data['main']['feels_like'])
                    # prepare output messages
                    out = []
                    foutstr = 'Сейчас в городе ' + cls.city + ' ' + str(temperature) + ' °C'
                    soutstr = 'Ощущается как ' + str(temperature_feels) + ' °C'
                    out.append(foutstr)
                    out.append(soutstr)
                    # log successful execution
                    logging.info('The wetherpredictor.predict method has completed successfully')
                    return out
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in wetherpredictor.predict: ' + str(e))
            return 'проблемы с сервисом'
