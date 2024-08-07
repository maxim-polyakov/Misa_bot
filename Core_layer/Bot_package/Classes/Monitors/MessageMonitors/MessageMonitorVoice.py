from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitor

class MessageMonitorVoice(MessageMonitor.MessageMonitor):
    """

    This class describes object for monitoring messages from chats

    """
    def __init__(self, message):
        MessageMonitorVoice.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, 'voice')