from Front_layer import telegram_bot
from Core_layer.Bot_package.Monitors import MessageMonitorTelegram

@telegram_bot.dp.message_handler(content_types=['text'])
async def get_user_text_EDA(message):


    mon = MessageMonitorTelegram.MessageMonitorTelegram(message)
    try:
        await telegram_bot.boto.send_message(message.chat.id, mon.monitor(), parse_mode='html')
    except:
        pass
