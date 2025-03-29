from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor
import validators

@discord_bot.bot.slash_command(name='play_song', description='Проиграть музыку')
async def play(message, *, url):
#
#
    await message.response.defer(ephemeral=True)
    if validators.url(url):
        if url.count('youtube'):
            sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
            out = await sm.join()
            if out != 'вы не подключены к голосовому каналу':
                out = await sm.monitor(url)
        else:
            out = 'проигрывается только youtube'
    else:
        out = 'некорректный url'
    await message.followup.send(out)

@discord_bot.bot.slash_command(name='pause', description='Ставит на паузу проигрывание музыки')
async def pause(message):
#
#
    await message.response.defer(ephemeral=True)
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    out = await sm.pause()
    await message.followup.send(out)

@discord_bot.bot.slash_command(name='stop', description='Отстанавливает проигрывание музыки')
async def stop(message):
#
#
    await message.response.defer(ephemeral=True)
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    out = await sm.stop()
    await message.followup.send(out)

@discord_bot.bot.slash_command(name='queue', description='Ставит музыку в очередь на исполнение')
async def queue(message, *, url):
#
#
    await message.response.defer(ephemeral=True)
    if validators.url(url):
        if url.count('youtube'):
            sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
            out = await sm.queue(url)
        else:
            out = 'проигрывается только youtube'
    else:
        out = 'некорректный url'
    await message.followup.send(out)

@discord_bot.bot.slash_command(name='resume', description='Возобновляет проигрывание музыки')
async def resume(message):
#
#
    await message.response.defer(ephemeral=True)
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    out = await sm.resume()
    await message.followup.send(out)
