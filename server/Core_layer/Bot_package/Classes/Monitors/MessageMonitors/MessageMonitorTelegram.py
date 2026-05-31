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
        MessageMonitorTelegram.__chat_id = (
            f'telegram_{message.chat.id}' if getattr(message, 'chat', None) else None
        )

    @classmethod
    def monitor(cls):
        return super().monitor(
            cls.__message, cls.__user, cls.__command, 'telegram', chat_id=cls.__chat_id
        )
