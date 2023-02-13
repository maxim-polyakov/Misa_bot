from Front_layer import telegram_bot
from Core_layer.Bot_package.Token import Classes

@telegram_bot.dp.message_handler(commands=['token'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        message.text = message.text.replace('/token ', '')

        Classes.Token.add_token(message.text)