import nest_asyncio
import Front_layer.discord_bot as db
from Core_layer.Test_package.PythonTests import TestRun as PyTest
from Core_layer.Bot_package.Token import Token
from Front_layer.discord_bot import messagemonitor

# ______________________________________________________________________________

if __name__ == "__main__":


    tkn = Token.Token()
    test = PyTest.TestRun()
    test.run_all_tests()
    df = tkn.get_token('select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Discord\'')
    token = df['token'][0]
    nest_asyncio.apply()
    db.bot.run(token)
