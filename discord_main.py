import sys
import Front_layer.discord_bot as db
from Core_layer.Test_package import PythonTests as PyTest
from Front_layer.discord_bot import messagemonitor
# ______________________________________________________________________________



if __name__ == "__main__":
    test = PyTest.TestRun()
    test.run_all_tests()

    token = ''
    db.nest_asyncio.apply()
    db.bot.run(token)

