import Front_layer.telegram_bot as tb
from Core_layer.Test_package.PythonTests import TestRun as PyTest
from Front_layer.telegram_bot import assistantmonitor
from Front_layer.telegram_bot import botoclean
from Front_layer.telegram_bot.bototrain import lstmtrain, rftrain, nbtrain
from Front_layer.telegram_bot import testmonitor
from Front_layer.telegram_bot import messagemonitor

# _______________________________________________________________________________
if __name__ == "__main__":
    test = PyTest.TestRun()
    test.run_all_tests()
    bot_process = tb.Process(target=tb.bot_start_polling)
    bot_process.start()
    tb.app.run()
