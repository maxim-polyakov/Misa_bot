import Front_layer.discord_bot as db
import flask
from Core_layer.Test_package.PythonTests import TestRun as PyTest
from Front_layer.discord_bot import messagemonitor

# ______________________________________________________________________________

if __name__ == "__main__":
#
#
    test = PyTest.TestRun()
    test.run_all_tests()
    bot_process = db.Process(target=db.bot_start_polling)
    bot_process.start()
    db.app.run()

