import discord
import nest_asyncio
import flask
from multiprocessing import Process
from Core_layer.Bot_package.Token import Token

from discord.ext import commands

config = {
    'prefix': '/',
    'intents': discord.Intents.default()
}
config['intents'].message_content = True

bot = commands.Bot(command_prefix=config['prefix'], intents=config['intents'])

config = {
    'prefix': '/',
    'intents': discord.Intents.default()
}
config['intents'].message_content = True

bot = commands.Bot(command_prefix=config['prefix'], intents=config['intents'])
APP_HOST = '127.0.0.1'
APP_PORT = '8999'
tkn = Token.Token()
df = tkn.get_token('select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Discord\'')
token = df['token'][0]


app = flask.Flask(__name__)

def bot_start_polling():
    bot.run(token)
