from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitor

@telegram_bot.dp.message_handler(content_types=['photo'])
async def download_photo(message):
    await message.photo[-1].download(destination_dir=(''))
    picMon = PictureMonitor.PictureMonitor()
    res = picMon.monitor()
    photo = 'resphotos/' + str(res)
    await telegram_bot.boto.send_photo(message.chat.id,
                                       photo=open(photo, 'rb'))
