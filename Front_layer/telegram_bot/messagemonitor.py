from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorTelegram


@telegram_bot.dp.message_handler(content_types=['text'])
async def get_user_text(message):
#
#
    mon = MessageMonitorTelegram.MessageMonitorTelegram(message)
    output = mon.monitor()
    if(output != ''):
        await telegram_bot.boto.send_message(message.chat.id, output, parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

