from abc import ABC, abstractmethod
from Core_layer.Bot_package.Interfaces import IWeather
from Deep_layer.API_package.Classes.WeatherPredictors import WeatherPredictor
import logging
import requests
import os

class Weather(IWeather.IWeather):
    """

    That's a class weather. It describes a weather prediction algorithm.

    """
    message_text = None
    def __init__(self, message_text):
        Weather.message_text = message_text
    @classmethod
    def predict(cls):
        # weather predict
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # create an instance of weatherpredictor with the given city name
            wp = WeatherPredictor.WetherPredictor(city=cls.message_text)
            # get the weather prediction result
            res = wp.predict()
            # if the result is not none, format and return it
            if res != None:
                out = str(res[0] + '. ' + res[1])
                # log successful completion of the prediction process
                logging.info('The drawer.predict process has completed successfully')
                return out
            else:
                return 'проблемы с сервисом, возможно город не найден'
        except Exception as e:
            # log any exceptions that occur during the prediction process
            logging.exception(str('The exception occurred in drawer.predict: ' + str(e)))
