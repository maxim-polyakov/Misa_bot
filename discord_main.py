import Front_layer.discord_bot as db
from Core_layer.Test_package import PythonTests as PyTest
import nest_asyncio
from Front_layer.discord_bot import assistantmonitor
from Front_layer.discord_bot import messagemonitor
# ______________________________________________________________________________

if __name__ == "__main__":
    test = PyTest.TestRun()
    test.run_all_tests()

    token = 'MTAzMDkzNTg1ODI4ODc4NzQ1Ng.GwoRou.XJTp0eeZZL70371_oCPEzNu7kO1nxelRXTADn8'
    nest_asyncio.apply()
    db.bot.run(token)

