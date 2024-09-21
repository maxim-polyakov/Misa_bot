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
    def monitor(cls, message, ptype):
        language = 'ru'

        audio_paths = 'audios/test.wav'
        if ptype == 'discord':
            myobj = gTTS(text=message.content, lang=language, slow=False)

        else:
            myobj = gTTS(text=message.text, lang=language, slow=False)

        if not os.path.isdir("audios"):
            os.mkdir("audios")
        myobj.save(audio_paths)
        player = discord.FFmpegOpusAudio(audio_paths, **cls.ffmpeg_options)
        id = message.guild.id
        cls.voice_clients[id].play(player)