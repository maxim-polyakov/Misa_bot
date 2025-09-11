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
        # picture monitor for discord
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if there are any attachments in the message
            if len(cls.message.attachments) > 0:
                attachment = cls.message.attachments[0]
                # check if the attachment is an image file (supported formats: jpg, jpeg, png, webp, gif)
                if (
                        attachment.filename.endswith(".jpg")
                        or attachment.filename.endswith(".jpeg")
                        or attachment.filename.endswith(".png")
                        or attachment.filename.endswith(".webp")
                        or attachment.filename.endswith(".gif")
                ):
                    # create a directory named "photos" if it does not exist
                    if not os.path.isdir("photos"):
                        os.mkdir("photos")
                    # get the list of files in the "photos" directory
                    total_con = os.listdir('photos')
                    # count the number of existing files to generate a unique filename
                    count = len(total_con)
                    # download the image from the attachment url
                    img_data = requests.get(attachment.url).content
                    # define the file path and temporary file name
                    file = "photos/file_" + str(count) + ".jpg"
                    tmp = "file_" + str(count) + ".jpg"
                    # save the downloaded image to the specified file
                    with open(file, "wb") as handler:
                        handler.write(img_data)
                    # log successful completion of the process
                    logging.info('The picturemonitordiscord.monitor process has completed successfully')
                    # call the parent class's monitor method with the file path and temporary file name
                    return super().monitor(file, tmp)
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception(str('The exception occurred in picturemonitordiscord.monitor: ' + str(e)))
