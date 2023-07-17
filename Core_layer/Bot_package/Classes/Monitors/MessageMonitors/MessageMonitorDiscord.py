import Front_layer.telegram_bot as telegram_bot
from Core_layer.Command_package.Commands import CommandAnalyzer
from Core_layer.Bot_package.Classes.Monitors import MessageMonitors

class MessageMonitorDiscord(MessageMonitors.MessageMonitor):

    def __init__(self, message):
        MessageMonitorDiscord.__command = CommandAnalyzer.CommandAnalyzer(
            telegram_bot.boto, message, 'discord')
        MessageMonitorDiscord.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command, 'discord')
