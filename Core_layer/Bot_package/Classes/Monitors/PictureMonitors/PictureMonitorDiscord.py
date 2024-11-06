import os
import requests
import logging
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitor


class PictureMonitorDiscord(PictureMonitor.PictureMonitor):
    """

    It is child of picture monitor for discord

    """
    def __init__(self, message):
        PictureMonitorDiscord.message = message

    @classmethod
    def monitor(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if len(cls.message.attachments) > 0:
                attachment = cls.message.attachments[0]

                if (
                        attachment.filename.endswith(".jpg")
                        or attachment.filename.endswith(".jpeg")
                        or attachment.filename.endswith(".png")
                        or attachment.filename.endswith(".webp")
                        or attachment.filename.endswith(".gif")
                ):
                    if not os.path.isdir("photos"):
                        os.mkdir("photos")

                    total_con = os.listdir('photos')

                    count = len(total_con)

                    img_data = requests.get(attachment.url).content
                    file = "photos/file_" + str(count) + ".jpg"
                    tmp = "file_" + str(count) + ".jpg"
                    with open(file, "wb") as handler:
                        handler.write(img_data)
                    logging.info('The picturemonitordiscord.monitor is done')
                    return super().monitor(file, tmp)
        except Exception as e:
            logging.exception(str('The exception in picturemonitordiscord.monitor ' + str(e)))
