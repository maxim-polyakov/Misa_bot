from abc import ABC, abstractmethod
from Core_layer.Bot_package.Interfaces import IDrawer
from Deep_layer.IOD_package.Classes import Dalle
from Deep_layer.Storage_package.Classes.S3Storage import upload_image
import logging
import requests
import os

class Drawer(IDrawer.IDrawer):
    """

    That's a class drawer. It describes an image drawing algorithm.
    Сохраняет изображения в S3 (Yandex Object Storage) или локально в images/ при отсутствии S3.

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
            image_bytes = p.content

            # Пробуем загрузить в S3
            s3_url = upload_image(image_bytes)
            if s3_url:
                logging.info('The drawer.draw process has completed successfully (S3)')
                return s3_url

            # Fallback: сохраняем локально
            if not os.path.exists('images'):
                os.makedirs('images')
            filepath = 'images/misaimg.png'
            if os.path.exists(filepath):
                os.remove(filepath)
            with open(filepath, 'wb') as out:
                out.write(image_bytes)
            logging.info('The drawer.draw process has completed successfully (local)')
            return filepath

        except Exception as e:
            logging.exception('The exception occurred in drawer.draw: ' + str(e))
            return None
