from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Finder import GoogleFinder


@discord_bot.bot.slash_command(name='find', description='Найти что то в гугле')
async def find(message, subject):
#
#
    await message.channel.send('Выполняется команда')
    name = message.message.author.name
    cl = GoogleFinder.GoogleFinder(subject)
    out = cl.find()
    await message.channel.send(out)
    await message.channel.send('Готово')