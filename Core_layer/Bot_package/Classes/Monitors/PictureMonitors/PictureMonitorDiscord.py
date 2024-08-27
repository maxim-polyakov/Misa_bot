from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitor
import cv2
import os
import requests

class PictureMonitorDiscord(PictureMonitor.PictureMonitor):
    """

    Summary

    """
    def __init__(self, message):
        PictureMonitorDiscord.message = message

    @classmethod
    def monitor(cls):


        if len(cls.message.attachments) > 0:
            attachment = cls.message.attachments[0]

            if (
                    attachment.filename.endswith(".jpg")
                    or attachment.filename.endswith(".jpeg")
                    or attachment.filename.endswith(".png")
                    or attachment.filename.endswith(".webp")
                    or attachment.filename.endswith(".gif")
            ):
                # Load the image
                total_con = os.listdir('photos')
                # font
                count = len(total_con)

                img_data = requests.get(attachment.url).content
                file = "photos/file_" + str(count) + ".jpg"
                tmp = "file_" + str(count) + ".jpg"
                with open(file, "wb") as handler:
                    handler.write(img_data)

                return super().monitor(file, tmp)