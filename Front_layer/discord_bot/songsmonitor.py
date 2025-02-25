from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor


@discord_bot.bot.slash_command(name='play_song', description='Проиграть музыку')
async def play(message, *, url):
#
#
    await message.response.defer(ephemeral=True)
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.join()
    await sm.monitor(url)
    await message.followup.send('готово')

@discord_bot.bot.slash_command(name='pause', description='Ставит на паузу проигрывание музыки')
async def pause(message):
#
#
    await message.response.defer(ephemeral=True)
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.pause()
    await message.followup.send('готово')

@discord_bot.bot.slash_command(name='stop', description='Отстанавливает проигрывание музыки')
async def stop(message):
#
#
    await message.response.defer(ephemeral=True)
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.stop()
    await message.followup.send('готово')

@discord_bot.bot.slash_command(name='queue', description='Ставит музыку в очередь на исполнение')
async def queue(message, *, url):
#
#
    await message.response.defer(ephemeral=True)
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    out = await sm.queue(url)
    await message.followup.send(out.lower())

@discord_bot.bot.slash_command(name='resume', description='Возобновляет проигрывание музыки')
async def resume(message):
#
#
    await message.response.defer(ephemeral=True)
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.resume()
    await message.followup.send('готово')
