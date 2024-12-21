from abc import ABC, abstractmethod
from Core_layer.Bot_package.Interfaces import IDrawer
from Deep_layer.IOD_package.Classes import Dalle
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
        image_url = cls.__dal.generate(cls.message_text)
        p = requests.get(image_url)
        if not os.path.exists('images'):
            os.makedirs('images')
        filepath = 'images/misaimg.png'
        out = open(filepath, 'wb')
        out.write(p.content)
        out.close()
        return filepath
