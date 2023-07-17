import Front_layer.telegram_bot as telegram_bot
from Core_layer.Command_package.Commands import CommandAnalyzer
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitor

class MessageMonitorDiscord(MessageMonitor.MessageMonitor):

    def __init__(self, message):
        MessageMonitorDiscord.__command = CommandAnalyzer.CommandAnalyzer(
            telegram_bot.boto, message, 'discord')
        MessageMonitorDiscord.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command, 'discord')
