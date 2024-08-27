from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitorTelegram
import os
@telegram_bot.dp.message_handler(content_types=['photo'])
async def download_photo(message):
    picMon = PictureMonitorTelegram.PictureMonitor(message)
    res = await picMon.monitor()
    photo = 'resphotos/' + str(res)
    await telegram_bot.boto.send_photo(message.chat.id,
                                       photo=open(photo, 'rb'))
