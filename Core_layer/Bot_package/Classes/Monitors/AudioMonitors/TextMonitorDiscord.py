import torch
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import TextMonitor


class TextMonitorDiscord(TextMonitor.TextMonitor):
    """

    Summary

    """
    def __init__(self, message):
        TextMonitorDiscord.__message = message

    @classmethod
    def monitor(cls, outstr):
        return super().monitor(cls.__message,'discord', outstr)
