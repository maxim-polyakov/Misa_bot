from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Bototrainers import XGBtrain
from pathlib import Path

@telegram_bot.dp.message_handler(commands='XGBtrain')
async def get_user_text(message):
    try:
        if (message.chat.username == 'The_Baxic'):

            xgb = XGBtrain.XGBtrain()
            await xgb.hitrain()
            await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')

            await xgb.thtrain()
            await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')

            await xgb.businesstrain()
            await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')

            await xgb.weathertrain()
            await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')

            await xgb.trashtrain()
            await telegram_bot.boto.send_message(message.chat.id, 'trashtrain', parse_mode='html')

            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass

@telegram_bot.dp.message_handler(commands='RFweathertrain')
async def get_user_text(message):
    try:
        if (message.chat.username == 'The_Baxic'):
            xgb = XGBtrain.XGBtrain()

            await xgb.weathertrain()
            await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass

@telegram_bot.dp.message_handler(commands='RFtrashtrain')
async def get_user_text(message):
    try:
        if (message.chat.username == 'The_Baxic'):
            xgb = XGBtrain.XGBtrain()

            await xgb.trashtrain()
            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass

@telegram_bot.dp.message_handler(commands='RFhitrain')
async def get_user_text(message):
    try:
        if (message.chat.username == 'The_Baxic'):
            xgb = XGBtrain.XGBtrain()

            await xgb.hitrain()
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
            xgb = XGBtrain.XGBtrain()

            await xgb.thtrain()
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
            xgb = XGBtrain.XGBtrain()

            await xgb.businesstrain()
            await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')
            pass
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
            xgb = XGBtrain.XGBtrain()

            await xgb.emotionstrain()
            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass