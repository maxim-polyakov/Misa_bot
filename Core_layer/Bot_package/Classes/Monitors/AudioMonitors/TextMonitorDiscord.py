import torch
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import TextMonitor

class TextMonitorDiscord(TextMonitor.TextMonitor):
    """

    Summary

    """

    device = torch.device('cpu')

    local_file = 'Deep_layer/NLP_package/models/model.pt'

    def __init__(self, message):
        TextMonitorDiscord.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message,'discord')
