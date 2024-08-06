from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.SongsMonitors import YTDLSource
import discord
import yt_dlp

@discord_bot.bot.command(name='play_song', help='To play song')
async def play(ctx, url):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send('You are not in a voice channel!')
        return

    voice_channel = ctx.author.voice.channel

    try:
        server = ctx.message.guild
        voice_client = server.voice_client

        if voice_client is None:
            voice_client = await voice_channel.connect()

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,  # Меньше выводить информации в консоль
            'noplaylist': True,  # Не загружать плейлисты
            'nocheckcertificate': True,  # Не проверять сертификаты SSL
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['url']

        vc = discord_bot.bot.voice_clients

        if voice_client and voice_client.is_connected():
            vc.play(discord_bot.discord.FFmpegPCMAudio(URL))
            await ctx.send(f'Now playing: {url}')
        else:
            pass
    except Exception as e:
        await ctx.send(f'An error occurred while playing the music: {e}')


@discord_bot.bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@discord_bot.bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")
@discord_bot.bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")