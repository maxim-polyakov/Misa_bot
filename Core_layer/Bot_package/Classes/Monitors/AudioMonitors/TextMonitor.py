# V4
from gtts import gTTS
import discord
import os
import logging
from Core_layer.Bot_package.Interfaces import IMonitor

class TextMonitor(IMonitor.IMonitor):
    """

    Summary

    """

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn -filter:a "volume=0.25"'}
    voice_clients = {}

    @classmethod
    async def join(cls, message):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            voice_client = await message.author.voice.channel.connect(timeout=500, reconnect=True)
            cls.voice_clients[voice_client.guild.id] = voice_client
            return cls.voice_clients[voice_client.guild.id]
            logging.info('The textmonitor.join is done')
        except Exception as e:
            logging.exception(str('The exception in textmonitor.join ' + str(e)))

    @classmethod
    async def monitor(cls, message, ptype, outstr):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            language = 'ru'

            audio_paths = 'audios/test.mp3'
            myobj = gTTS(text=outstr, lang=language, slow=False)

            if not os.path.isdir("audios"):
                os.mkdir("audios")
            myobj.save(audio_paths)
            player = discord.FFmpegOpusAudio(audio_paths)
            id = message.guild.id
            cls.voice_clients[id].play(player)
            logging.info('The textmonitor.monitor is done')
        except Exception as e:
            logging.exception(str('The exception in textmonitor.join ' + str(e)))