from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.DataCleaners import MemoryCleaner


@discord_bot.bot.slash_command(name='clean', description='Леманатизировать таблицу в баз данных по имени')
async def clean(message, tablename):
#
#
    await message.channel.send('Выполняется команда')
    name = message.message.author.name
    strr = tablename
    cl = MemoryCleaner.MemoryCleaner(strr)
    cl.clean()
    await message.channel.send('Готово')