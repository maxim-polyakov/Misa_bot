from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.DataCleaners import MemoryCleaner


@discord_bot.bot.slash_command(name='clean', help='Леманатизировать таблицу в баз данных по имени')
async def clean(message, table):
#
#
    name = message.message.author.name
    if (name == 'seraphim8341'):
        strr = table
        cl = MemoryCleaner.MemoryCleaner(strr)
        cl.clean()
        await message.channel.send('cleaned')
    else:
        await message.channel.send('😊')