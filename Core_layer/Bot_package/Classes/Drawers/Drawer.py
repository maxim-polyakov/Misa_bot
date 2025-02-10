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
        # drawing images by dalle
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # generate an image url using the __dal object
            image_url = cls.__dal.generate(cls.message_text)
            # send a request to download the image
            p = requests.get(image_url)
            # check if the 'images' directory exists, if not, create it
            if not os.path.exists('images'):
                os.makedirs('images')
            # define the file path to save the image
            filepath = 'images/misaimg.png'
            # open the file in write-binary mode and save the image content
            out = open(filepath, 'wb')
            out.write(p.content)
            out.close()
            # log successful completion of the draw process
            logging.info('The drawer.draw process is completed successfully')
            # return the file path of the saved image
            return filepath
        except Exception as e:
            # log any exceptions that occur during the process
            logging.exception('The exception occurred in drawer.draw: ' + str(e))
