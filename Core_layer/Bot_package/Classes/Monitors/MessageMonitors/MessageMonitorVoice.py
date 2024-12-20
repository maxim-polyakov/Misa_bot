from Core_layer.Command_package.Classes.Commands import CommandAnalyzer
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitor


class MessageMonitorVoice(MessageMonitor.MessageMonitor):
    """

    This class describes object for monitoring messages from chats

    """
    def __init__(self, boto, message):
        MessageMonitorVoice.__command = CommandAnalyzer.CommandAnalyzer(boto,
            message, 'audio')
        MessageMonitorVoice.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command,'voice')