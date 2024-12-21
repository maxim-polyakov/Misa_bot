from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Drawers import Drawer

@telegram_bot.dp.message_handler(commands=['calculate'])
async def get_user_text(message):
    #
    #
    if (message.chat.username == 'The_Baxic'):
        inpt = message.text.replace('/draw ', '')
        draw = Drawer.Drawer(message.text.lower())
        outputder = draw.draw()
        photo = str(outputder)
        await telegram_bot.boto.send_photo(message.chat.id, photo=open(photo, 'rb'))
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')