from abc import ABC, abstractmethod
from Core_layer.Bot_package.Interfaces import IDrawer
from Deep_layer.IOD_package.Classes import Dalle
from Deep_layer.Storage_package.Classes.S3Storage import upload_image
import logging
import requests
import os
import time

class Drawer(IDrawer.IDrawer):
    """

    That's a class drawer. It describes an image drawing algorithm.
    Сохраняет изображения в S3 (Yandex Object Storage) или локально в images/ при отсутствии S3.
    source: 'telegram'|'discord' — помечает для регулярной очистки.

    """
    message_text = None
    __source = None
    __dal = Dalle.Dalle()
    def __init__(self, text, source=None):
        Drawer.message_text = text
        Drawer.__source = source if source in ('telegram', 'discord') else None

    @classmethod
    def draw(cls):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        attempt = 0
        while True:
            try:
                attempt += 1
                image_url = cls.__dal.generate(cls.message_text)
                p = requests.get(image_url)
                image_bytes = p.content

                # Пробуем загрузить в S3 (source=telegram/discord для пометки под очистку)
                s3_url = upload_image(image_bytes, source=cls.__source)
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
                logging.warning(f'drawer.draw attempt {attempt} failed: {e}')
                time.sleep(2)
