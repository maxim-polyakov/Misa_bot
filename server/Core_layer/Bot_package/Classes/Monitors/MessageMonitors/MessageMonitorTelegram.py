from Core_layer.Command_package.Classes.Commands import CommandAnalyzer
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitor


class MessageMonitorTelegram(MessageMonitor.MessageMonitor):
    """

    This class describes object for monitoring messages from chats

    """
    def __init__(self, boto, user, message):
        MessageMonitorTelegram.__command = CommandAnalyzer.CommandAnalyzer(boto,
            message, 'telegram')
        MessageMonitorTelegram.__message = message
        MessageMonitorTelegram.__user = user

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__user, cls.__command,'telegram')
