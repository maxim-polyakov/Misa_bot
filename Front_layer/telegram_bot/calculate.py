from Front_layer import telegram_bot
from Core_layer.Command_package.Classes.CommandActions import CommandAction


@telegram_bot.dp.message_handler(commands=['calculate'])
async def get_user_text(message):
    #
    #
    if (message.chat.username == 'The_Baxic'):
        inpt = message.text.replace('/calculate ', '')
        calc = CommandAction.CommandAction(message, inpt)
        outputder = calc.eighth()
        await telegram_bot.boto.send_message(message.chat.id, outputder, parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
