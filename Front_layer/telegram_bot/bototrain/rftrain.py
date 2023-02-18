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
        # resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
        # message.text = message.text.replace('/LSTMweathertrain ', ' ')
        # lt = LSTMtrain.LSTMtrain()
        # message_text_array = message.text.split()
        #
        # if (len(message.text) > 0):
        #     epochs = message_text_array.pop(0)
        # else:
        #     epochs = 200
        #
        # lt.weathertrain((int(epochs)))
        # await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')
        # await telegram_bot.boto.send_photo(message.chat.id,
        #                                photo=open(resultrainingpath, 'rb'))
        #
        # await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFtrashtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        # resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
        # message.text = message.text.replace('/LSTMtrashtrain ', ' ')
        # lt = LSTMtrain.LSTMtrain()
        # message_text_array = message.text.split()
        #
        # if (len(message.text) > 0):
        #     epochs = message_text_array.pop(0)
        # else:
        #     epochs = 200
        #
        # lt.trashtrain(int(epochs))
        # await telegram_bot.boto.send_message(message.chat.id, 'trashtrain', parse_mode='html')
        # await telegram_bot.boto.send_photo(message.chat.id,
        #                                photo=open(resultrainingpath, 'rb'))
        #
        # await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFhitrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        # resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
        # message.text = message.text.replace('/LSTMhitrain ', ' ')
        # lt = LSTMtrain.LSTMtrain()
        # message_text_array = message.text.split()
        #
        # if (len(message.text) > 0):
        #     epochs = message_text_array.pop(0)
        # else:
        #     epochs = 200
        #
        # lt.hitrain(int(epochs))
        # await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')
        # await telegram_bot.boto.send_photo(message.chat.id,
        #                                    photo=open(resultrainingpath, 'rb'))
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFthtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        # resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
        # message.text = message.text.replace('/LSTMthtrain ', ' ')
        # lt = LSTMtrain.LSTMtrain()
        # message_text_array = message.text.split()
        #
        # if (len(message.text) > 0):
        #     epochs = message_text_array.pop(0)
        # else:
        #     epochs = 200
        #
        # lt.thtrain(int(epochs))
        # await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')
        # await telegram_bot.boto.send_photo(message.chat.id,
        #                                    photo=open(resultrainingpath, 'rb'))
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFbusinesstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        # resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
        # message.text = message.text.replace('/LSTMbusinesstrain ', ' ')
        # lt = LSTMtrain.LSTMtrain()
        # message_text_array = message.text.split()
        #
        # if(len(message.text) > 0):
        #     epochs = message_text_array.pop(0)
        # else:
        #     epochs = 200
        #
        # lt.businesstrain(int(epochs))
        #
        # await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')
        # await telegram_bot.boto.send_photo(message.chat.id,
        #                                    photo=open(resultrainingpath, 'rb'))
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='RFemotionstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        # message.text = message.text.replace('/LSTMemotionstrain ', ' ')
        # lt = LSTMtrain.LSTMtrain()
        # message_text_array = message.text.split()
        # if(len(message.text) > 0):
        #     epochs = message_text_array.pop(0)
        # else:
        #     epochs = 200
        # lt.emotionstrain(int(epochs))
        # resultrainingpath = next(Path().rglob('resultstraining_multy.png'))
        # telegram_bot.boto.send_photo(message.chat.id,
        #                            photo=open(resultrainingpath, 'rb'))
        # await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        pass
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
