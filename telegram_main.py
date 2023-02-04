import Front_layer.telegram_bot as tb
from Core_layer.Test_package import PythonTests as PyTest
from aiogram import executor
from Front_layer.telegram_bot import assistantmonitor
from Front_layer.telegram_bot import botoclean
from Front_layer.telegram_bot import bototrain
from Front_layer.telegram_bot import messagemonitor

# _______________________________________________________________________________
if __name__ == "__main__":
    test = PyTest.TestRun()
    test.run_all_tests()
    executor.start_polling(tb.dp, skip_updates=True)
