from Core_layer.Bot_package.Interfaces import IMonitor
import yt_dlp
import asyncio
import discord
import urllib.parse, urllib.request, re
class SongsMonitor(IMonitor.IMonitor):
    """

    Summary

    """

    queues = {}
    voice_clients = {}
    youtube_base_url = 'https://www.youtube.com/'
    youtube_results_url = youtube_base_url + 'results?'
    youtube_watch_url = youtube_base_url + 'watch?v='
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn -filter:a "volume=0.25"'}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)


    def __init__(self, bot, message):
        SongsMonitor.bot = bot
        SongsMonitor.message = message

    @classmethod
    async def __play_next(cls, message):
        if cls.queues[message.guild.id] != []:
            link = cls.queues[message.guild.id].pop(0)
            sm = SongsMonitor(cls.bot, message)
            await sm.monitor(link)

    @classmethod
    async def join(cls):
        try:
            voice_client = await cls.message.author.voice.channel.connect()
            cls.voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

    @classmethod
    async def leave(cls):
        server = cls.message.message.guild
        voice_client = server.voice_client
        await voice_client.disconnect()

    @classmethod
    async def queue(cls, url):
        if cls.message.guild.id not in cls.queues:
            cls.queues[cls.message.guild.id] = []
        cls.queues[cls.message.guild.id].append(url)
        out = "Added to queue!"
        return out

    @classmethod
    async def stop(cls):
        voice_client = cls.message.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await cls.message.send("The bot is not playing anything at the moment.")

    @classmethod
    async def pause(cls):
        voice_client = cls.message.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await cls.message.send("The bot is not playing anything at the moment.")

    @classmethod
    async def resume(cls):
        try:
            cls.voice_clients[cls.message.guild.id].resume()
        except Exception as e:
            print(e)

    @classmethod
    async def monitor(cls, url):
        try:
            if cls.youtube_base_url not in url:
                query_string = urllib.parse.urlencode({
                    'search_query': url
                })

                content = urllib.request.urlopen(
                    cls.youtube_results_url + query_string
                )

                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

                cls.url = cls.youtube_watch_url + search_results[0]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: cls.ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **cls.ffmpeg_options)
            id = cls.message.guild.id
            cls.voice_clients[id].play(player,
                                   after=lambda e: asyncio.run_coroutine_threadsafe(cls.__play_next(cls.message),
                                                                                    cls.bot.loop))
        except Exception as e:
            print(e)
