from Core_layer.Bot_package.Interfaces import IMonitor
import cv2
import os
import requests

class PictureMonitor(IMonitor.IMonitor):
    """

    Summary

    """
    def __init__(self, message):
        PictureMonitor.message = message

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
                tmp = ''
                # font
                count = len(total_con)
                font = cv2.FONT_HERSHEY_SIMPLEX
                # fontScale
                fontScale = 1
                # Blue color in BGR
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2
                images = []
                face_classifier = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                )

                img_data = requests.get(attachment.url).content
                file = "photos/file_" + str(count + 1) + ".jpg"
                tmp = "file_" + str(count + 1) + ".jpg"
                with open(file, "wb") as handler:
                    handler.write(img_data)

                total_con = os.listdir('photos')

                image = cv2.imread(file, cv2.COLOR_BGR2GRAY)
                images.append(image)

                for image in images:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags=cv2.CASCADE_SCALE_IMAGE)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        cv2.putText(image, 'Face', (x, y), font,
                                    fontScale, color, thickness, cv2.LINE_AA)

                dir_name = 'resphotos'
                os.makedirs(dir_name, exist_ok=True)
                filename = 'resphotos/' + tmp
                cv2.imwrite(filename, image)
                return filename