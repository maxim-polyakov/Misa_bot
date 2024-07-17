from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.DataCleaners import MemoryCleaner

@telegram_bot.dp.message_handler(commands=['clean'])
async def get_user_text(message):
#
#
    if (message.chat.username == 'The_Baxic'):
        strr = message.text.replace('/clean ', '')
        cl = MemoryCleaner.MemoryCleaner(strr)
        cl.clean()
        await telegram_bot.boto.send_message(message.chat.id, 'cleaned', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands=['clean'])
async def get_user_text(message):
#
#
    if (message.chat.username == 'The_Baxic'):
        strr = message.text.replace('/clean ', '')
        cl = MemoryCleaner.MemoryCleaner(strr)
        cl.clean()
        await telegram_bot.boto.send_message(message.chat.id, 'cleaned', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')