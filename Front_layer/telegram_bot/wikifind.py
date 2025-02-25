from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Finder import WikiFinder


@telegram_bot.dp.message_handler(commands=['wikifind'])
async def get_user_text(message):
#
#
    input = message.text.replace('/wikifind ', '')
    found = WikiFinder.WikiFinder(message_text=input)
    res = found.find()
    await telegram_bot.boto.send_message(message.chat.id, res.lower())

