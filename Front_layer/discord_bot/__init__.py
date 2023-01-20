import discord
from discord.ext import commands
import nest_asyncio


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


