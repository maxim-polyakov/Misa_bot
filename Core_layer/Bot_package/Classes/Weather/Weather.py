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
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            wp = WeatherPredictor.WetherPredictor(city=cls.message_text)
            res = wp.predict()
            if res != None:
                out = str(res[0] + '. ' + res[1])
                logging.info('The drawer.predict is done')
                return out
        except Exception as e:
            logging.exception(str('The exception in drawer.predict ' + str(e)))
