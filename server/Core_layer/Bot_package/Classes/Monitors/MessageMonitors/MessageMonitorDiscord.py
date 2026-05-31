from Core_layer.Command_package.Classes.Commands import CommandAnalyzer
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitor


class MessageMonitorDiscord(MessageMonitor.MessageMonitor):
    """

    This class describes object for monitoring messages from chats

    """
    def __init__(self, boto, user, message):
        MessageMonitorDiscord.__command = CommandAnalyzer.CommandAnalyzer(boto,
            message, 'discord')
        MessageMonitorDiscord.__message = message
        MessageMonitorDiscord.__user = user
        MessageMonitorDiscord.__chat_id = (
            f'discord_{message.channel.id}' if message.channel else None
        )

    @classmethod
    def monitor(cls):
        return super().monitor(
            cls.__message, cls.__user, cls.__command, 'discord', chat_id=cls.__chat_id
        )
