from Front_layer import telegram_bot
from Deep_layer.API_package.Classes.Translators import MemoryTranslator
from Core_layer.Command_package.Classes.CommandActions import CommandAction


@telegram_bot.dp.message_handler(commands=['translate'])
async def get_user_text(message):
#
#
    if (message.chat.username == 'The_Baxic'):
        input = message.text.replace('/translate ', '')
        traslated = CommandAction.CommandAction(message, input)
        res = traslated.translate()
        await telegram_bot.boto.send_message(message.chat.id, res)
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊')
