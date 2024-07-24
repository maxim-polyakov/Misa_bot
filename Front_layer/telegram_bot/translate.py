from Front_layer import telegram_bot
from Core_layer.API_package.Classes.Translators import GoogleTranslator


@telegram_bot.dp.message_handler(commands=['translate'])
async def get_user_text(message):
#
#
    if (message.chat.username == 'The_Baxic'):
        input = message.text.replace('/translate ', '')
        traslated = GoogleTranslator.GoogleTranslator("ru")
        res = traslated.translate(input)
        await telegram_bot.boto.send_message(message.chat.id, res, parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
