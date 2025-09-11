from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import TextMonitor


class TextMonitorDiscord(TextMonitor.TextMonitor):
    """

    It is a child of text monitor for discord

    """
    def __init__(self, message):
        TextMonitorDiscord.__message = message

    @classmethod
    def monitor(cls, outstr):
        # calls the parent class's 'monitor' method with specific parameters
        return super().monitor(cls.__message,'discord', outstr)
