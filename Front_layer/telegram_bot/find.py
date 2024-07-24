from Front_layer import telegram_bot
from Core_layer.API_package.Classes.Finders import WikiFinder


@telegram_bot.dp.message_handler(commands=['find'])
async def get_user_text(message):
#
#
    if (message.chat.username == 'The_Baxic'):
        input = message.text.replace('/find ', '')
        found = WikiFinder.WikiFinder()
        res = found.find(input)
        await telegram_bot.boto.send_message(message.chat.id, res, parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
