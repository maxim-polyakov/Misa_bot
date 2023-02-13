from Front_layer import telegram_bot
from Core_layer.Bot_package.Token import Token

@telegram_bot.dp.message_handler(commands=['token'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        message.text = message.text.replace('/token ', '')

        Token.Token.add_token(message.text)