from Front_layer import telegram_bot
from Core_layer.Bot_package.Bototrainers import RFTrain
from pathlib import Path

@telegram_bot.dp.message_handler(commands='RFtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):

        rt = RFTrain.RFtrain()
        rt.hitrain()
        await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')

        rt.thtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')

        rt.businesstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')

        rt.weathertrain()
        await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')

        rt.trashtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trashtrain', parse_mode='html')

        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFweathertrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        rt = RFTrain.RFtrain()

        rt.weathertrain()
        await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFtrashtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        rt = RFTrain.RFtrain()

        rt.trashtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFhitrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        rt = RFTrain.RFtrain()

        rt.hitrain()
        await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFthtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        rt = RFTrain.RFtrain()

        rt.thtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFbusinesstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        rt = RFTrain.RFtrain()

        rt.businesstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFemotionstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        rt = RFTrain.RFtrain()
        
        rt.emotionstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
