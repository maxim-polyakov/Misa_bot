from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Finder import WikiFinder


@discord_bot.bot.slash_command(name='wikifind', description='Найти что то в википедии')
async def wikifind(message, subject):
#
#
    await message.response.defer(ephemeral=True)
    cl = WikiFinder.WikiFinder(subject)
    out = cl.find()
    await message.followup.send(out)
