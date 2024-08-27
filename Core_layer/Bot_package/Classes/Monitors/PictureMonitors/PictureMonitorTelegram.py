from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitor
import cv2
import os

class PictureMonitorTelegram(PictureMonitor.PictureMonitor):
    """

    Summary

    """
    def __init__(self, message):
        PictureMonitorTelegram.message = message

    @classmethod
    async def monitor(cls):

        total_con = os.listdir('photos')
        count = len(total_con)
        file = "photos/file_" + str(count) + ".jpg"
        tmp = "file_" + str(count) + ".jpg"
        await cls.message.photo[-1].download((file))

        return super().monitor(file, tmp)