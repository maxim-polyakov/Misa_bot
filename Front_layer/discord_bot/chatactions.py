import os
from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor


def remove_all_files(dir):
#
#
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

@discord_bot.bot.slash_command(name='join', description='Подключится к каналу')
async def join(message):
#
#
    await message.channel.send('Выполняется команда')
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.join()
    await message.channel.send('Готово')

@discord_bot.bot.slash_command(name='leave', description='Выйти из канала')
async def leave(message):
#
#
    await message.channel.send('Выполняется команда')
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.leave()
    await message.channel.send('Готово')
