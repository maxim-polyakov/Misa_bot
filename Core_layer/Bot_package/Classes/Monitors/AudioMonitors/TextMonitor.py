# V4
from gtts import gTTS
import discord
import os
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
        try:
            voice_client = await message.author.voice.channel.connect()
            cls.voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

    @classmethod
    async def monitor(cls, message, ptype):
        language = 'ru'

        audio_paths = 'audios/test.mp3'
        if ptype == 'discord':
            myobj = gTTS(text=message.content, lang=language, slow=False)

        else:
            myobj = gTTS(text=message.text, lang=language, slow=False)

        if not os.path.isdir("audios"):
            os.mkdir("audios")
        myobj.save(audio_paths)
        player = discord.FFmpegOpusAudio(audio_paths)
        id = message.guild.id
        cls.voice_clients[id].play(player)