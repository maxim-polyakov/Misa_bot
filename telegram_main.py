import Front_layer.telegram_bot as tb
from Core_layer.Test_package.Classes.PythonTests import TestRun as PyTest

# _______________________________________________________________________________
if __name__ == "__main__":
#
#
    test = PyTest.TestRun()
    test.run_all_tests()
    bot_process = tb.Process(target=tb.bot_start_polling)
    bot_process.start()


