import Front_layer.telegram_bot as telegram_bot
from Core_layer.Command_package.Classes.Commands import CommandAnalyzer
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitor

class MessageMonitorTelegram(MessageMonitor.MessageMonitor):


    def __init__(self, message):
        MessageMonitorTelegram.__command = CommandAnalyzer.CommandAnalyzer(
            telegram_bot.boto, message, 'telegram')
        MessageMonitorTelegram.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command, 'telegram')
