from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Drawers import Drawer

@telegram_bot.dp.message_handler(commands=['draw'])
async def get_user_text(message):
    inpt = message.text.replace('/draw ', '')
    draw = Drawer.Drawer(inpt)
    outputder = draw.draw()
    if not outputder:
        await telegram_bot.boto.send_message(message.chat.id, 'Не удалось сгенерировать изображение')
        return
    # S3 URL или локальный путь
    if str(outputder).startswith('http'):
        await telegram_bot.boto.send_photo(message.chat.id, photo=outputder)
    else:
        await telegram_bot.boto.send_photo(message.chat.id, photo=open(outputder, 'rb'))
