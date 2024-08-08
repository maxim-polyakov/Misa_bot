from Front_layer import discord_bot
import yt_dlp
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor

queues = {}
voice_clients = {}
youtube_base_url = 'https://www.youtube.com/'
youtube_results_url = youtube_base_url + 'results?'
youtube_watch_url = youtube_base_url + 'watch?v='
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)


async def play_next(message):
    if queues[message.guild.id] != []:
        link = queues[message.guild.id].pop(0)
        await play(message, link=link)

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
