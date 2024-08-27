from Core_layer.Bot_package.Interfaces import IMonitor
import cv2
import os
import requests

class PictureMonitor(IMonitor.IMonitor):
    """

    Summary

    """
    i = 0
    def __init__(self, message):
        PictureMonitor.message = message

    @classmethod
    def monitor(cls):
        pass