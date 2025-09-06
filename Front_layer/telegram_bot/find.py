from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Finder import GoogleFinder


@telegram_bot.dp.message_handler(commands=['find'])
async def get_user_text(message):
#
#
    input = message.text.replace('/find ', '')
    found = GoogleFinder.GoogleFinder(message_text=input)
    res = found.find()
    await telegram_bot.boto.send_message(message.chat.id, res)

