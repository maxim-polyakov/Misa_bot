import torch
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import TextMonitor

class TextMonitorDiscord(TextMonitor.TextMonitor):
    """

    Summary

    """
    def __init__(self, message, outstr):
        TextMonitorDiscord.__message = message
        TextMonitorDiscord.__outstr = outstr

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message,'discord', cls.__outstr)
