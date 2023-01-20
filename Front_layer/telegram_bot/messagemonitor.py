from Front_layer import telegram_bot
from Core_layer.Bot_package import Monitors


@telegram_bot.dp.message_handler(content_types=['text'])
async def get_user_text(message):
    mon = Monitors.MessageMonitorTelegram(message)
    outstr = mon.monitor()
    try:
        await telegram_bot.boto.send_message(message.chat.id, outstr, parse_mode='html')
    except:
        pass
