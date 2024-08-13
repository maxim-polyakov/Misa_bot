from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitor
from Core_layer.Command_package.Classes.Commands import CommandAnalyzer

class MessageMonitorVoice(MessageMonitor.MessageMonitor):
    """

    This class describes object for monitoring messages from chats

    """
    def __init__(self, message):
        MessageMonitorVoice.__command = CommandAnalyzer.CommandAnalyzer(
            message, 'audio')
        MessageMonitorVoice.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command,'voice')