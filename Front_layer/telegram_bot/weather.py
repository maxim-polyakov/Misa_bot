from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Weather import Weather


@telegram_bot.dp.message_handler(commands=['weather'])
async def get_user_text(message):
#
#
    if (message.chat.username == 'The_Baxic'):
        city = message.text.replace('/weather ', '')
        wp = Weather.Weather(message_text=city)
        res = wp.predict()
        await telegram_bot.boto.send_message(message.chat.id, res, parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')