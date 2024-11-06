from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor


@discord_bot.bot.command(name='play_song', help='To play song')
async def play(message, *, url):
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.join()
    await sm.monitor(url)

@discord_bot.bot.command(name='pause', help='This command pauses the song')
async def pause(message):
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.pause()

@discord_bot.bot.command(name='stop', help='Stops the song')
async def stop(message):
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.stop()

@discord_bot.bot.command(name="queue")
async def queue(message, *, url):
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    out = await sm.queue(url)
    await message.send(out)

@discord_bot.bot.command(name="resume")
async def resume(message):
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.resume()
