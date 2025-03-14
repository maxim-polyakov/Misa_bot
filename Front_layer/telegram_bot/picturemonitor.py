import os
from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitorTelegram

@telegram_bot.dp.message_handler(content_types=['photo'])
async def download_photo(message):
#
#
    try:
        lowertext = message.html_text.lower()
    except:
        lowertext = 'None'
    if (lowertext.count('миса') > 0
        or lowertext.lower().count('misa') > 0
        or lowertext.count('миша') > 0
        or lowertext.count('misha') > 0
        or lowertext.count('миса,') > 0
        or lowertext.count('иса') > 0):
        picMon = PictureMonitorTelegram.PictureMonitorTelegram(message)
        res = await picMon.monitor()
        photo = str(res)
        await telegram_bot.boto.send_photo(message.chat.id,
                                        photo=open(photo, 'rb'))
