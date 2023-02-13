import Front_layer.telegram_bot as telegram_bot
from Core_layer.Command_package.Commands import Classes
from Core_layer.Bot_package.Monitors import Abstract_classes

class MessageMonitorDiscord(Abstract_classes.MessageMonitor):

    def __init__(self, message):
        MessageMonitorDiscord.__command = Classes.CommandAnalyzer(
            telegram_bot.boto, message, 'discord')
        MessageMonitorDiscord.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command, 'discord')

class MessageMonitorTelegram(Abstract_classes.MessageMonitor):

    def __init__(self, message):
        MessageMonitorTelegram.__command = Classes.CommandAnalyzer(
            telegram_bot.boto, message, 'telegram')
        MessageMonitorTelegram.__message = message

    @classmethod
    def monitor(cls):
        return super().monitor(cls.__message, cls.__command, 'telegram')