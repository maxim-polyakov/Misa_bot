from Front_layer import telegram_bot
from Deep_layer.API_package.Classes.WeatherPredictors import WeatherPredictor


@telegram_bot.dp.message_handler(commands=['weather'])
async def get_user_text(message):
#
#
    if (message.chat.username == 'The_Baxic'):
        city = message.text.replace('/weather ', '')
        wp = WeatherPredictor.WetherPredictor(city)
        wp = wp.predict()
        await telegram_bot.boto.send_message(message.chat.id, wp[0], parse_mode='html')
        await telegram_bot.boto.send_message(message.chat.id, wp[1], parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')