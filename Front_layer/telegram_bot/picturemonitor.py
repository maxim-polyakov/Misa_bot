import os
from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitorTelegram

@telegram_bot.dp.message_handler(content_types=['photo'])
async def download_photo(message):
    picMon = PictureMonitorTelegram.PictureMonitorTelegram(message)
    res = await picMon.monitor()
    photo =  str(res)
    await telegram_bot.boto.send_photo(message.chat.id,
                                       photo=open(photo, 'rb'))
