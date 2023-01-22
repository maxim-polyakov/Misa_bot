from Front_layer import telegram_bot
from Core_layer.Bot_package import DataCleaners

@telegram_bot.dp.message_handler(commands=['clean'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        strr = message.text.replace('/clean ','')
        cl = DataCleaners.MisaMemoryCleater(strr)
        cl.clean()
        await telegram_bot.boto.send_message(message.chat.id, 'cleaned', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
