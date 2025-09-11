from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Finder import WikiFinder
import os

@discord_bot.bot.slash_command(name='wikifind', description='Найти что то в википедии')
async def wikifind(message, subject):
#
#
    await message.response.defer(ephemeral=True)
    cl = WikiFinder.WikiFinder(subject)
    out = cl.find()
    if (len(out) > 2000):
        if not os.path.exists('txtfiles'):
            os.makedirs('txtfiles')
        with open('txtfiles/message.txt', 'w+', encoding='utf-8') as file:
            file.write(out)
        await message.followup.send(file=discord_bot.disnake.File('txtfiles/message.txt'))
    else:
        await message.followup.send(out)
