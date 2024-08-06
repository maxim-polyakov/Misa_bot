from Core_layer.Bot_package.Interfaces import IMonitor
import cv2
import os

class PictureMonitor(IMonitor.IMonitor):
    """

    Summary

    """
    @classmethod
    def monitor(cls):
        # Load the image
        total_con = os.listdir('photos')
        tmp = ''
        count = len(total_con)
        # font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # fontScale
        fontScale = 1
        # Blue color in BGR
        color = (255, 0, 0)
        # Line thickness of 2 px
        thickness = 2
        faces = []
        images = []
        face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        for con in total_con:
            image = cv2.imread("photos/" + con, cv2.COLOR_BGR2GRAY)
            images.append(image)
            tmp = con
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