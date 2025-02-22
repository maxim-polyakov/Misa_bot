from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Finder import GoogleFinder


@discord_bot.bot.slash_command(name='find', description='Найти что то в гугле')
async def find(message, subject):
#
#
    if message.author != discord_bot.bot.user:
        name = message.message.author.name
        cl = GoogleFinder.GoogleFinder(subject)
        out = cl.find()
        await message.channel.send(out)