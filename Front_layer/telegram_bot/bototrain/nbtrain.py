from Front_layer import telegram_bot
from Core_layer.Bot_package.Bototrainers import NBTrain
from pathlib import Path


@telegram_bot.dp.message_handler(commands='RFtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):

        nbt = NBTrain.NBTrain()
        nbt.hitrain()
        await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')

        nbt.thtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')

        nbt.businesstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')

        nbt.weathertrain()
        await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')

        nbt.trashtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trashtrain', parse_mode='html')

        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFweathertrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        nbt.weathertrain()
        await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFtrashtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        nbt.trashtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFhitrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        nbt.hitrain()
        await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFthtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        nbt.thtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFbusinesstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        nbt.businesstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFemotionstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        nbt.emotionstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')