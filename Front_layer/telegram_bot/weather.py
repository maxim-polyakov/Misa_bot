from Front_layer import telegram_bot
from Core_layer.Command_package.Classes.CommandActions import CommandAction


@telegram_bot.dp.message_handler(commands=['weather'])
async def get_user_text(message):
#
#
    if (message.chat.username == 'The_Baxic'):
        city = message.text.replace('/weather ', '')
        wp = CommandAction.CommandAction(message, city)
        res = wp.weather()
        await telegram_bot.boto.send_message(message.chat.id, res, parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')