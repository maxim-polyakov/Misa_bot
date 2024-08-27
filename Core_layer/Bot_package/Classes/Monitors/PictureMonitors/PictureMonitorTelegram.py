from Core_layer.Bot_package.Interfaces import IMonitor
import cv2
import os

class PictureMonitor(IMonitor.IMonitor):
    """

    Summary

    """
    def __init__(self, message):
        PictureMonitor.message = message

    @classmethod
    async def monitor(cls):

        total_con = os.listdir('photos')
        count = len(total_con)
        file = "photos/file_" + str(count) + ".jpg"
        tmp = "file_" + str(count) + ".jpg"
        await cls.message.photo[-1].download((file))
        # font
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
        return tmp