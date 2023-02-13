from Front_layer import telegram_bot
from Core_layer.Test_package import TestMonitors
from Core_layer.Bot_package.ValidsetAnalizers import Classes

@telegram_bot.dp.message_handler(commands=['testmonitor'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
         tmonlstm = TestMonitors.TestMonitorLSTM()
         tmonlstm.monitor()
         an = Classes.ValidsetAlanizer()
         analizedict = an.analize()
         maxanalizedict = max(analizedict.values())[0]
         LSTMACC = analizedict['LSTMACC'][0]
         await telegram_bot.boto.send_message(message.chat.id, 'Наибольшая точность ' + str(maxanalizedict) +
                               ', LSTM_Acc ' + LSTMACC,
                               parse_mode='html')
    else:
         await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands=['analyze'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
         an = Classes.ValidsetAlanizer()
         analizedict = an.analize('analyzetable')
         maxanalizedict = max(analizedict.values())[0]
         LSTMACC = analizedict['LSTMACC'][0]
         await telegram_bot.boto.send_message(message.chat.id, 'Наибольшая точность ' + str(maxanalizedict) +
                               ', LSTM_Acc ' + LSTMACC,
                               parse_mode='html')
    else:
         await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands=['LSTMmonitor'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
         tmonlstm = TestMonitors.TestMonitorLSTM()
         tmonlstm.monitor()
         await telegram_bot.boto.send_message(message.chat.id, 'ready', parse_mode='html')
    else:
         await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands=['NaiveBayesmonitor'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
         tmonnb = TestMonitors.TestMonitorNaiveBayes()
         tmonnb.monitor()
         await telegram_bot.boto.send_message(message.chat.id, 'ready', parse_mode='html')
    else:
         await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands=['RandomForestmonitor'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
         tmonrf = TestMonitors.TestMonitorRandomForest()
         tmonrf.monitor()
         await telegram_bot.boto.send_message(message.chat.id, 'ready', parse_mode='html')
    else:
         await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands=['XGBoostmonitor'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
         tmonxgboost = TestMonitors.TestMonitorXGBoost()
         tmonxgboost.monitor()
         await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
         await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

@telegram_bot.dp.message_handler(commands=['Combinemonitor'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
         tmoncomb = TestMonitors.TestMonitorCombine()
         tmoncomb.monitor()
         await telegram_bot.boto.send_message(message.chat.id, 'trained', parse_mode='html')
    else:
         await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')

