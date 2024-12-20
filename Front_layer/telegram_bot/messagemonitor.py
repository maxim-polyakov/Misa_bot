from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorTelegram


@telegram_bot.dp.message_handler(content_types=['text'])
async def get_user_text(message):
#
#
    mon = MessageMonitorTelegram.MessageMonitorTelegram(telegram_bot.boto, message)
    output = mon.monitor()
    if(output != '' or output != '\n'):
        try:
            if message.text.lower().count('нарисуй') > 0:
                output = output.replace('\n', '')
                photo = str(output)
                await telegram_bot.boto.send_photo(message.chat.id, photo=open(photo, 'rb'))
            else:
                await telegram_bot.boto.send_message(message.chat.id, output, parse_mode='html')
        except Exception as e:
            pass
