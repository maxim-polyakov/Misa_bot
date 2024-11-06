import logging
import os
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitor


class PictureMonitorTelegram(PictureMonitor.PictureMonitor):
    """

    It is child of picture monitor for telegram

    """
    def __init__(self, message):
        PictureMonitorTelegram.message = message

    @classmethod
    async def monitor(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            total_con = os.listdir('photos')
            count = len(total_con)
            file = "photos/file_" + str(count) + ".jpg"
            tmp = "file_" + str(count) + ".jpg"
            await cls.message.photo[-1].download((file))
            logging.info('The picturemonitortelegram.monitor is done')
            return super().monitor(file, tmp)
        except Exception as e:
            logging.exception(str('The exception in picturemonitortelegram.monitor ' + str(e)))
