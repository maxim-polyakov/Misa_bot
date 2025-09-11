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
        # picture monitor for telegram
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # get the list of files in the 'photos' directory
            total_con = os.listdir('photos')
            # count the number of files in the directory
            count = len(total_con)
            # define the file path for the new image
            file = "photos/file_" + str(count) + ".jpg"
            tmp = "file_" + str(count) + ".jpg"
            # download the last received photo and save it to the defined path
            await cls.message.photo[-1].download((file))
            # log successful completion of the monitoring process
            logging.info('The picturemonitortelegram.monitor process has completed successfully')
            # call the parent class's monitor method with the new file path
            return super().monitor(file, tmp)
        except Exception as e:
            # log any exceptions that occur during the process
            logging.exception('The exception occurred in picturemonitortelegram.monitor: ' + str(e))
