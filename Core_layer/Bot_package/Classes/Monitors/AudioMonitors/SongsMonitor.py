import yt_dlp
import asyncio
import discord
import logging
import urllib.parse, urllib.request, re
from Core_layer.Bot_package.Interfaces import IMonitor


class SongsMonitor(IMonitor.IMonitor):
    """

    It is class for playing music

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
        # play next song
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if there are songs in the queue for the guild
            if cls.queues[message.guild.id] != []:
                # get the next song link from the queue
                link = cls.queues[message.guild.id].pop(0)
                # create an instance of songsmonitor
                sm = SongsMonitor(cls.bot, message)
                # log that the play_next function is executed
                logging.info('The songsmonitor.__play_next process is completed successfully')
                # start monitoring the song
                await sm.monitor(link)
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in songsmonitor.__play_next: ' + str(e))


    @classmethod
    async def join(cls):
        # join to the channel
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # connect to the voice channel of the message author
            voice_client = await cls.message.author.voice.channel.connect()
            # store the voice client instance in the dictionary with the guild id as the key
            cls.voice_clients[voice_client.guild.id] = voice_client
            # log successful connection
            logging.info('The songsmonitor.join method has completed successfully')
        except Exception as e:
            # log any exceptions that occur during the connection process
            logging.exception('The exception occurred in songsmonitor.join: ' + str(e))

    @classmethod
    async def leave(cls):
        # leave from the channel
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # get the server (guild) from the message
            server = cls.message.message.guild
            # get the voice client associated with the server
            voice_client = server.voice_client
            # disconnect the bot from the voice channel
            await voice_client.disconnect()
            # log successful disconnection
            logging.info('The songsmonitor.leave method has completed successfully')
        except Exception as e:
            # log the exception with details
            logging.exception('The exception occurred in songsmonitor.leave: ' + str(e))

    @classmethod
    async def queue(cls, url):
        # add song to the queue
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if the guild (server) has an existing queue
            if cls.message.guild.id not in cls.queues:
                cls.queues[cls.message.guild.id] = []
            # add the song url to the queue
            cls.queues[cls.message.guild.id].append(url)
            out = "Added to queue!"
            # log successful queue addition
            logging.info('The songsmonitor.queue method has completed successfully')
            return out
        except Exception as e:
            # log any exceptions that occur
            logging.exception('The exception occurred in songsmonitor.queue: ' + str(e))

    @classmethod
    async def stop(cls):
        # stop playing song
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # get the voice client for the current guild
            voice_client = cls.message.message.guild.voice_client
            # check if the bot is currently playing audio
            if voice_client.is_playing():
                await voice_client.stop()
            else:
                await cls.message.send("The bot is not playing anything at the moment.")
            # log successful execution
            logging.info('The songsmonitor.stop method has completed successfully')
        except Exception as e:
            # log any exceptions that occur
            logging.exception('The exception occurred in songsmonitor.stop: ' + str(e))

    @classmethod
    async def pause(cls):
        # pause the currently playing song
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # get the voice client for the current guild
            voice_client = cls.message.message.guild.voice_client
            # check if the bot is currently playing audio
            if voice_client.is_playing():
                # pause the playback
                await voice_client.pause()
            else:
                # inform the user that nothing is currently playing
                await cls.message.send("The bot is not playing anything at the moment.")
            # log successful execution of the pause method
            logging.info('The songsmonitor.pause method has completed successfully')
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in songsmonitor.pause: ' + str(e))


    @classmethod
    async def resume(cls):
        # resume currently playing song
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # resume playback for the voice client associated with the guild
            cls.voice_clients[cls.message.guild.id].resume()
            logging.info('The songsmonitor.resume method has completed successfully')
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in songsmonitor.resume: ' + str(e))

    @classmethod
    async def monitor(cls, url):
        # playing songs
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if the provided url is not a direct youtube link
            if cls.youtube_base_url not in url:
                # convert the search query into a url-encoded format
                query_string = urllib.parse.urlencode({
                    'search_query': url
                })
                # fetch search results from youtube
                content = urllib.request.urlopen(
                    cls.youtube_results_url + query_string
                )
                # extract video ids from the search results
                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())
                # construct the full youtube video url
                cls.url = cls.youtube_watch_url + search_results[0]
            # get the current event loop
            loop = asyncio.get_event_loop()
            # run the youtube downloader in an executor (non-blocking)
            data = await loop.run_in_executor(None, lambda: cls.ytdl.extract_info(url, download=False))
            # extract the direct audio url from the downloaded data
            song = data['url']
            # create an ffmpeg audio player for discord
            player = discord.FFmpegOpusAudio(song, **cls.ffmpeg_options)
            # get the guild (server) id
            id = cls.message.guild.id
            # play the audio in the corresponding voice client
            cls.voice_clients[id].play(player,
                                   after=lambda e: asyncio.run_coroutine_threadsafe(cls.__play_next(cls.message),
                                                                                    cls.bot.loop))
            # log successful execution
            logging.info('The songsmonitor.monitor method has completed successfully')
        except Exception as e:
            # log any exceptions that occur
            logging.exception('The exception occurred in songsmonitor.monitor: ' + str(e))
