from Front_layer import discord_bot
import yt_dlp
import asyncio
import urllib.parse, urllib.request, re

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
        try:
            voice_client = await message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)
        try:
            if youtube_base_url not in url:
                query_string = urllib.parse.urlencode({
                    'search_query': url
                })

                content = urllib.request.urlopen(
                    youtube_results_url + query_string
                )

                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

                link = youtube_watch_url + search_results[0]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

            song = data['url']
            player = discord_bot.discord.FFmpegOpusAudio(song, **ffmpeg_options)
            id = message.guild.id
            voice_clients[id].play(player,
                                            after=lambda e: asyncio.run_coroutine_threadsafe(play_next(message), discord_bot.bot.loop))
        except Exception as e:
            print(e)

@discord_bot.bot.command(name='pause', help='This command pauses the song')
async def pause(message):
    voice_client = message.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await message.send("The bot is not playing anything at the moment.")

@discord_bot.bot.command(name='resume', help='Resumes the song')
async def resume(message):
    voice_client = message.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await message.send("The bot was not playing anything before this. Use play_song command")
@discord_bot.bot.command(name='stop', help='Stops the song')
async def stop(message):
    voice_client = message.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await message.send("The bot is not playing anything at the moment.")