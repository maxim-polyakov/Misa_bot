from Front_layer import telegram_bot
from Core_layer.Bot_package.Bototrainers import RFTrain
from pathlib import Path

@telegram_bot.dp.message_handler(commands='RFtrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):

            rt = RFTrain.RFtrain()
            await rt.hitrain()
            await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')

            await rt.thtrain()
            await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')

            await rt.businesstrain()
            await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')

            await rt.weathertrain()
            await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')

            await rt.trashtrain()
            await telegram_bot.boto.send_message(message.chat.id, 'trashtrain', parse_mode='html')

            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='RFweathertrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            rt = RFTrain.RFtrain()

            await rt.weathertrain()
            await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='RFtrashtrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            rt = RFTrain.RFtrain()
            await rt.trashtrain()
            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='RFhitrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            rt = RFTrain.RFtrain()
            await rt.hitrain()
            await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='RFthtrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            rt = RFTrain.RFtrain()
            await rt.thtrain()
            await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='RFbusinesstrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            rt = RFTrain.RFtrain()

            await rt.businesstrain()
            await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='RFemotionstrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            rt = RFTrain.RFtrain()

            await rt.emotionstrain()
            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass
