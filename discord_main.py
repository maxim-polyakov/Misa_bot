import Front_layer.discord_bot as db
from Core_layer.Test_package import PythonTests as PyTest
from Core_layer.Bot_package import Token
import nest_asyncio
# ______________________________________________________________________________

if __name__ == "__main__":
    tkn = Token.Token()
    test = PyTest.TestRun()
    test.run_all_tests()
    df = tkn.get_token('select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Discord\'')
    token = df['token'][0]
    nest_asyncio.apply()
    db.bot.run(token)

