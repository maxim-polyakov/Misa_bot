from Front_layer import telegram_bot
from Core_layer.Bot_package import Bototrainers

@telegram_bot.dp.message_handler(commands='emotionstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        lt = Bototrainers.LSTMtrain()
        bt = Bototrainers.NaiveBayesTrain()
        rt = Bototrainers.RandomForestTrain()
        xt = Bototrainers.XgboostTrain()
        bt.emotionstrain()
        rt.emotionstrain()
        xt.emotionstrain()
        lt.emotionstrain(30)
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='LSTMemotionstrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        message.text = message.text.replace('/LSTMemotionstrain ', ' ')
        lt = Bototrainers.LSTMtrain()
        message_text_array = message.text.split()
        if(len(message.text) > 0):
            epochs = message_text_array.pop(0)
        else:
            epochs = 200
        lt.emotionstrain(int(epochs))
        resultrainingpath = next(telegram_bot.Path().rglob('resultstraining_multy.png'))
        telegram_bot.boto.send_photo(message.chat.id,
                                   photo=open(resultrainingpath, 'rb'))
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands='LSTMtrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        resultrainingpath = next(telegram_bot.Path().rglob('resultstraining_binary.png'))
        message.text = message.text.replace('/LSTMtrain ', ' ')
        lt = Bototrainers.LSTMtrain()
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

@telegram_bot.dp.message_handler(commands='NaiveBayestrain')
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
        mt = Bototrainers.NaiveBayesTrain()
        mt.hitrain()
        mt.thtrain()
        mt.businesstrain()
        mt.weathertrain()
        mt.emotionstrain()
        await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')