from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Finder import DuckduckgoFinder


@discord_bot.bot.slash_command(name='find', description='Найти что то в гугле')
async def find(message, subject):
#
#
    await message.response.defer(ephemeral=True)
    cl = DuckduckgoFinder.DuckduckgoFinder(subject)
    out = cl.find()
    await message.followup.send(out)
