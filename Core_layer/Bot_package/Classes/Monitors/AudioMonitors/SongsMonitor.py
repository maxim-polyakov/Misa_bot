from Core_layer.Bot_package.Interfaces import IMonitor
import yt_dlp
import asyncio
import discord
import logging
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
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.queues[message.guild.id] != []:
                link = cls.queues[message.guild.id].pop(0)
                sm = SongsMonitor(cls.bot, message)
                logging.info('The songsmonitor.__play_next is done')
                await sm.monitor(link)
        except Exception as e:
            logging.exception(str('The exception in songsmonitor.__play_next ' + str(e)))


    @classmethod
    async def join(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            voice_client = await cls.message.author.voice.channel.connect()
            cls.voice_clients[voice_client.guild.id] = voice_client
            logging.info('The songsmonitor.join is done')
        except Exception as e:
            logging.exception(str('The exception in songsmonitor.join ' + str(e)))

    @classmethod
    async def leave(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            server = cls.message.message.guild
            voice_client = server.voice_client
            await voice_client.disconnect()
            logging.info('The songsmonitor.leave is done')
        except Exception as e:
            logging.exception(str('The exception in songsmonitor.leave ' + str(e)))

    @classmethod
    async def queue(cls, url):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message.guild.id not in cls.queues:
                cls.queues[cls.message.guild.id] = []
            cls.queues[cls.message.guild.id].append(url)
            out = "Added to queue!"
            logging.info('The songsmonitor.queue is done')
            return out
        except Exception as e:
            logging.exception(str('The exception in songsmonitor.queue ' + str(e)))

    @classmethod
    async def stop(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            voice_client = cls.message.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.stop()
            else:
                await cls.message.send("The bot is not playing anything at the moment.")
            logging.info('The songsmonitor.stop is done')
        except Exception as e:
            logging.exception(str('The exception in songsmonitor.queue ' + str(e)))

    @classmethod
    async def pause(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            voice_client = cls.message.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.pause()
            else:
                await cls.message.send("The bot is not playing anything at the moment.")
            logging.info('The songsmonitor.pause is done')
        except Exception as e:
            logging.exception(str('The exception in songsmonitor.pause ' + str(e)))


    @classmethod
    async def resume(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            cls.voice_clients[cls.message.guild.id].resume()
            logging.info('The songsmonitor.resume is done')
        except Exception as e:
            logging.exception(str('The exception in songsmonitor.resume ' + str(e)))

    @classmethod
    async def monitor(cls, url):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
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
            logging.info('The songsmonitor.monitor is done')
        except Exception as e:
            logging.exception(str('The exception in songsmonitor.monitor ' + str(e)))
