from Front_layer import telegram_bot
from Core_layer.Bot_package.Bototrainers import LSTMtrain
from pathlib import Path

@telegram_bot.dp.message_handler(commands='LSTMtrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
            message.text = message.text.replace('/LSTMtrain ', ' ')
            lt = LSTMtrain.LSTMtrain()
            message_text_array = message.text.split()

            if(len(message.text) > 0):
                epochs = message_text_array.pop(0)
            else:
                epochs = 200

            lt.hitrain(int(epochs))
            await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                               photo=open(resultrainingpath, 'rb'))

            if (len(message.text) > 0):
                if (message_text_array != []):
                    epochs = message_text_array.pop(0)
            else:
                pass

            lt.thtrain(int(epochs))
            await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                               photo=open(resultrainingpath, 'rb'))

            if (len(message.text) > 0):
                if (message_text_array != []):
                    epochs = message_text_array.pop(0)
            else:
                pass

            lt.businesstrain(int(epochs))

            await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                               photo=open(resultrainingpath, 'rb'))
            lt.weathertrain((int(epochs)))
            await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                               photo=open(resultrainingpath, 'rb'))
            lt.trashtrain(int(epochs))
            await telegram_bot.boto.send_message(message.chat.id, 'trashtrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                               photo=open(resultrainingpath, 'rb'))
            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')

        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='LSTMweathertrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
            message.text = message.text.replace('/LSTMweathertrain ', ' ')
            lt = LSTMtrain.LSTMtrain()
            message_text_array = message.text.split()

            if (len(message.text) > 0):
                epochs = message_text_array.pop(0)
            else:
                epochs = 200

            await lt.weathertrain((int(epochs)))
            await telegram_bot.boto.send_message(message.chat.id, 'weathertrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                           photo=open(resultrainingpath, 'rb'))

            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='LSTMtrashtrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
            message.text = message.text.replace('/LSTMtrashtrain ', ' ')
            lt = LSTMtrain.LSTMtrain()
            message_text_array = message.text.split()

            if (len(message.text) > 0):
                epochs = message_text_array.pop(0)
            else:
                epochs = 200

            lt.trashtrain(int(epochs))
            await telegram_bot.boto.send_message(message.chat.id, 'trashtrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                           photo=open(resultrainingpath, 'rb'))

            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='LSTMhitrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
            message.text = message.text.replace('/LSTMhitrain ', ' ')
            lt = LSTMtrain.LSTMtrain()
            message_text_array = message.text.split()

            if (len(message.text) > 0):
                epochs = message_text_array.pop(0)
            else:
                epochs = 200

            lt.hitrain(int(epochs))
            await telegram_bot.boto.send_message(message.chat.id, 'hitrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                               photo=open(resultrainingpath, 'rb'))
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='LSTMthtrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
            message.text = message.text.replace('/LSTMthtrain ', ' ')
            lt = LSTMtrain.LSTMtrain()
            message_text_array = message.text.split()

            if (len(message.text) > 0):
                epochs = message_text_array.pop(0)
            else:
                epochs = 200

            lt.thtrain(int(epochs))
            await telegram_bot.boto.send_message(message.chat.id, 'thtrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                               photo=open(resultrainingpath, 'rb'))
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='LSTMbusinesstrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            resultrainingpath = next(Path().rglob('resultstraining_binary.png'))
            message.text = message.text.replace('/LSTMbusinesstrain ', ' ')
            lt = LSTMtrain.LSTMtrain()
            message_text_array = message.text.split()

            if(len(message.text) > 0):
                epochs = message_text_array.pop(0)
            else:
                epochs = 200

            lt.businesstrain(int(epochs))

            await telegram_bot.boto.send_message(message.chat.id, 'businesstrain', parse_mode='html')
            await telegram_bot.boto.send_photo(message.chat.id,
                                               photo=open(resultrainingpath, 'rb'))
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass


@telegram_bot.dp.message_handler(commands='LSTMemotionstrain')
async def get_user_text(message):
#
#
    try:
        if (message.chat.username == 'The_Baxic'):
            message.text = message.text.replace('/LSTMemotionstrain ', ' ')
            lt = LSTMtrain.LSTMtrain()
            message_text_array = message.text.split()
            if(len(message.text) > 0):
                epochs = message_text_array.pop(0)
            else:
                epochs = 200
            lt.emotionstrain(int(epochs))
            resultrainingpath = next(Path().rglob('resultstraining_multy.png'))
            await telegram_bot.boto.send_photo(message.chat.id,
                                       photo=open(resultrainingpath, 'rb'))
            await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
        else:
            await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
    except:
        pass
