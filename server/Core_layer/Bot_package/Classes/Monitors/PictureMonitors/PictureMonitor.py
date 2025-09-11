import cv2
import os
import logging
from Core_layer.Bot_package.Interfaces import IMonitor


class PictureMonitor(IMonitor.IMonitor):
    """

    It is class for picture processing

    """
    def __init__(self, message):
        PictureMonitor.message = message

    @classmethod
    def monitor(cls, file, tmp):
        # monitor for images
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # define font settings for text overlay
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            images = []
            # load the pre-trained face detection model
            face_classifier = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            # read the input image and convert it to grayscale
            image = cv2.imread(file, cv2.COLOR_BGR2GRAY)
            images.append(image)
            # process each image in the list
            for image in images:
                # convert the image to grayscale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # detect faces in the image
                faces = face_classifier.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE)
                # draw rectangles around detected faces and add labels
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(image, 'Face', (x, y), font,
                                fontScale, color, thickness, cv2.LINE_AA)
                # create a directory to save the processed images
                dir_name = 'resphotos'
                os.makedirs(dir_name, exist_ok=True)
                # save the processed image with detected faces
                filename = 'resphotos/' + tmp
                cv2.imwrite(filename, image)
            # log successful completion of the function
            logging.info('The picturemonitor.monitor process has completed successfully')
            return filename
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception(str('The exception occurred in picturemonitor.monitor: ' + str(e)))
