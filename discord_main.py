import Front_layer.discord_bot as db
from Core_layer.Test_package.PythonTests import TestRun as PyTest
from Core_layer.Bot_package.Classes.Token import Token
from Front_layer.discord_bot.bototrain import lstmtrain
from Front_layer.discord_bot import messagemonitor

# ______________________________________________________________________________

if __name__ == "__main__":
#
#
    tkn = Token.Token()
    test = PyTest.TestRun()
    test.run_all_tests()
    bot_process = db.Process(target=db.bot_start_polling)
    bot_process.start()
    db.app.run(host='0.0.0.0', port=80)
