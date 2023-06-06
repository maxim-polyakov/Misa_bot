from Front_layer import telegram_bot
from Core_layer.Bot_package.Bototrainers import NBTrain
from pathlib import Path


@telegram_bot.dp.message_handler(commands='NBtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):

        nbt = NBTrain.NBTrain()
        await nbt.hitrain()
        await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')

        await nbt.thtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')

        await nbt.businesstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')

        await nbt.weathertrain()
        await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')

        await nbt.trashtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trashtrain', parse_mode='html')

        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFweathertrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        await nbt.weathertrain()
        await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFtrashtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        await nbt.trashtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFhitrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        await nbt.hitrain()
        await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFthtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        await nbt.thtrain()
        await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFbusinesstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        await nbt.businesstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands='RFemotionstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        nbt = NBTrain.NBTrain()

        await nbt.emotionstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')