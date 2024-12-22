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
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            image_url = cls.__dal.generate(cls.message_text)
            p = requests.get(image_url)
            if not os.path.exists('images'):
                os.makedirs('images')
            filepath = 'images/misaimg.png'
            out = open(filepath, 'wb')
            out.write(p.content)
            out.close()
            logging.info('The drawer.draw is done')
            return filepath
        except Exception as e:
            logging.exception(str('The exception in drawer.draw ' + str(e)))
