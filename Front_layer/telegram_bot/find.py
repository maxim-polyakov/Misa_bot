from Front_layer import telegram_bot
from Core_layer.Command_package.Classes.CommandActions import CommandAction


@telegram_bot.dp.message_handler(commands=['find'])
async def get_user_text(message):
#
#
    if (message.chat.username == 'The_Baxic'):
        input = message.text.replace('/find ', '')
        found = CommandAction.CommandAction(message, message_text=input)
        res = found.find()
        await telegram_bot.boto.send_message(message.chat.id, res, parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
