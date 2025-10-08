from abc import ABC, abstractmethod
from Core_layer.Bot_package.Interfaces import IDrawer
from Deep_layer.IOD_package.Classes import Dalle
import logging
import requests
import os

class Drawer(IDrawer.IDrawer):
    """

    That's a class drawer. It describes an image drawing algorithm.

    """
    message_text = None
    __dal = Dalle.Dalle()
    def __init__(self, text):
        Drawer.message_text = text

    @classmethod
    def draw(cls):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            image_url = cls.__dal.generate(cls.message_text)
            p = requests.get(image_url)

            if not os.path.exists('images'):
                os.makedirs('images')

            filepath = 'images/misaimg.png'

            # Удаляем старый файл если существует
            if os.path.exists(filepath):
                os.remove(filepath)

            # Создаём новый файл
            with open(filepath, 'wb') as out:
                out.write(p.content)

            logging.info('The drawer.draw process has completed successfully')
            return filepath

        except Exception as e:
            logging.exception('The exception occurred in drawer.draw: ' + str(e))
            return None
