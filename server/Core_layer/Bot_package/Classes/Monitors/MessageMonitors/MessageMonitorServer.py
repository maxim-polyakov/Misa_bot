from Core_layer.Command_package.Classes.Commands import CommandAnalyzer
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitor


class MessageMonitorServer(MessageMonitor.MessageMonitor):
    """

    This class describes object for monitoring messages from chats

    """
    def __init__(self, user, message, chat_id=None):
        MessageMonitorServer.__command = CommandAnalyzer.CommandAnalyzer('server',
            message, 'server')
        MessageMonitorServer.__message = message
        MessageMonitorServer.__user = user
        MessageMonitorServer.__chat_id = chat_id

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__user, cls.__command, 'server', chat_id=cls.__chat_id)
