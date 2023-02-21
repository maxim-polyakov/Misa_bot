from Front_layer import telegram_bot
from Core_layer.Test_package.TestMonitors import TestMonitorLSTM
from Core_layer.Test_package.TestMonitors import TestMonitorNB
from Core_layer.Test_package.TestMonitors import TestMonitorRF
from Core_layer.Test_package.TestMonitors import TestMonitorXGB

from Core_layer.Bot_package.ValidsetAnalizers import ValidsetAlanizer

@telegram_bot.dp.message_handler(commands=['testmonitor'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):

         tmonlstm = TestMonitorLSTM.TestMonitorLSTM()
         tmonlstm.monitor()

         tmonnb = TestMonitorNB.TestMonitorNB()
         tmonnb.monitor()

         tmonrf = TestMonitorRF.TestMonitorRF()
         tmonrf.monitor()

         tmonxgb = TestMonitorXGB.TestMonitorXGB()
         tmonxgb.monitor()

         an = ValidsetAlanizer.ValidsetAlanizer()
         analizedict = an.analyze()
         maxanalizedict = max(analizedict.values())[0]

         LSTMACC = analizedict['LSTMACC'][0]
         RFACC = analizedict['RFACC'][0]
         NBACC = analizedict['NBACC'][0]
         XGBACC = analizedict['XGBACC'][0]

         await telegram_bot.boto.send_message(message.chat.id,
                                              'Наибольшая точность '
                                              + str(maxanalizedict),
                                              parse_mode='html')
    else:
         await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


@telegram_bot.dp.message_handler(commands=['analyze'])
async def get_user_text(message):
    if (message.chat.username == 'The_Baxic'):
         an = ValidsetAlanizer.ValidsetAlanizer()
         analizedict = an.analyze('analyzetable')
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
         tmonlstm = TestMonitorLSTM.TestMonitorLSTM()
         tmonlstm.monitor()
         await telegram_bot.boto.send_message(message.chat.id, 'ready', parse_mode='html')
    else:
         await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')


