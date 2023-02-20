from Front_layer import telegram_bot
from Core_layer.Bot_package.Bototrainers import XGBtrain
from pathlib import Path

@telegram_bot.dp.message_handler(commands='XGBtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):

        xgb = XGBtrain.XGBtrain()
        xgb.hitrain()
        await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')

        xgb.thtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')

        xgb.businesstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')

        xgb.weathertrain()
        await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')

        xgb.trashtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trashtrain', parse_mode='html')

        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFweathertrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        xgb = XGBtrain.XGBtrain()

        xgb.weathertrain()
        await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFtrashtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        xgb = XGBtrain.XGBtrain()

        xgb.trashtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFhitrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        xgb = XGBtrain.XGBtrain()

        xgb.hitrain()
        await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFthtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        xgb = XGBtrain.XGBtrain()

        xgb.thtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFbusinesstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        xgb = XGBtrain.XGBtrain()

        xgb.businesstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFemotionstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        xgb = XGBtrain.XGBtrain()

        xgb.emotionstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
