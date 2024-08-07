import discord
import flask
from multiprocessing import Process
from discord.ext import commands,tasks
from Core_layer.Bot_package.Classes.Token import Token
import nest_asyncio

config = {
    'prefix': '!',
    'intents': discord.Intents.default()
}
config['intents'].message_content = True
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=config['prefix'], intents=config['intents'])
tkn = Token.Token()
df = tkn.get_token('select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Discord\'')
token = df['token'][0]
#token = "MTAzMDkzNTg1ODI4ODc4NzQ1Ng.G_P4SP.00QDwDA5wFvK1HJv2hYd2OeGbIAHg56HG_jLtQ"

app = flask.Flask(__name__)
def bot_start_polling():
    bot.run(token)
    #client.run(token)
    nest_asyncio.apply()
