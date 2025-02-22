from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor


@discord_bot.bot.slash_command(name='play_song', description='Проиграть музыку')
async def play(message, *, url):
#
#
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.join()
    await sm.monitor(url)

@discord_bot.bot.slash_command(name='pause', description='Ставит на паузу проигрывание музыки')
async def pause(message):
#
#
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.pause()

@discord_bot.bot.slash_command(name='stop', description='Отстанавливает проигрывание музыки')
async def stop(message):
#
#
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.stop()

@discord_bot.bot.slash_command(name='queue', description='Ставит музыку в очередь на исполнение')
async def queue(message, *, url):
#
#
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    out = await sm.queue(url)
    await message.send(out)

@discord_bot.bot.slash_command(name='resume', description='Возобновляет проигрывание музыки')
async def resume(message):
#
#
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.resume()
