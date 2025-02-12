# V4
from gtts import gTTS
import discord
import os
import logging
from Core_layer.Bot_package.Interfaces import IMonitor


class TextMonitor(IMonitor.IMonitor):
    """

    It is class for speaking

    """

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn -filter:a "volume=0.25"'}
    voice_clients = {}

    @classmethod
    async def join(cls, message):
        # join to the channel
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # connect to the voice channel of the message author
            voice_client = await message.author.voice.channel.connect(timeout=500, reconnect=True)
            # store the voice client instance in the dictionary with the guild id as the key
            cls.voice_clients[voice_client.guild.id] = voice_client
            # log successful connection
            logging.info('The textmonitor.join method has completed successfully')
            return cls.voice_clients[voice_client.guild.id]
        except Exception as e:
            logging.exception(str('The exception occurred in textmonitor.join: ' + str(e)))

    @classmethod
    async def monitor(cls, message, ptype, outstr):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # set the language for text-to-speech conversion
            language = 'ru'
            # define the path where the generated audio file will be saved
            audio_paths = 'audios/test.mp3'
            # convert the given text (outstr) to speech using gtts
            myobj = gTTS(text=outstr, lang=language, slow=False)
            # check if the "audios" directory exists, if not, create it
            if not os.path.isdir("audios"):
                os.mkdir("audios")
            # save the generated speech as an audio file
            myobj.save(audio_paths)
            # create a discord audio player using ffmpeg
            player = discord.FFmpegOpusAudio(audio_paths)
            # get the guild (server) id from the message
            id = message.guild.id
            # play the generated audio in the voice channel
            cls.voice_clients[id].play(player)
            # log successful execution
            logging.info('The textmonitor.monitor method has completed successfully')
        except Exception as e:
            logging.exception('The exception occurred in textmonitor.monitor: ' + str(e))
