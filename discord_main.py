import Front_layer.discord_bot as db
from Core_layer.Test_package.Classes.PythonTests import TestRun as PyTest
from Front_layer.discord_bot import botoclean
from Front_layer.discord_bot import chatactions
from Front_layer.discord_bot import songsmonitor
from Front_layer.discord_bot import messagemonitor

# ______________________________________________________________________________

if __name__ == "__main__":
#
#
    #tkn = Token.Token()
    test = PyTest.TestRun()
    test.run_all_tests()
    bot_process = db.Process(target=db.bot_start_polling)
    bot_process.start()
    db.app.run(host='127.0.0.1', port='8000')

