# V4
from gtts import gTTS
import discord
from Core_layer.Bot_package.Interfaces import IMonitor

class TextMonitor(IMonitor.IMonitor):
    """

    Summary

    """

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn -filter:a "volume=0.25"'}

    @classmethod
    def monitor(cls, message, ptype):
        language = 'ru'

        audio_paths = 'audios/test.wav'
        if ptype == 'discord':
            myobj = gTTS(text=message.content, lang=language, slow=False)
            myobj.save(audio_paths)
        else:
            myobj = gTTS(text=message.text, lang=language, slow=False)
            myobj.save(audio_paths)
        player = discord.FFmpegOpusAudio(audio_paths, **cls.ffmpeg_options)
        id = cls.message.guild.id
        cls.voice_clients[id].play(player)