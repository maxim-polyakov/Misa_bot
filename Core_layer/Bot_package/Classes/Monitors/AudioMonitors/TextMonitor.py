# V4
import os
import torch
import yt_dlp
import asyncio
import discord
import urllib.parse, urllib.request, re
from Core_layer.Bot_package.Interfaces import IMonitor

class TextMonitor(IMonitor.IMonitor):
    """

    Summary

    """

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn -filter:a "volume=0.25"'}

    @classmethod
    def monitor(cls, message, ptype):
        device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = 'model.pt'
        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                           local_file)
        model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        model.to(device)

        sample_rate = 48000
        speaker = 'baya'

        if ptype == 'discord':
            audio_paths = model.save_wav(audio_path='audios/test.wav',
                                        text=message.content,
                                        speaker=speaker,
                                        sample_rate=sample_rate
                                        )
            print(audio_paths)
        else:
            audio_paths = model.save_wav(audio_path='audios/test.wav',
                                        text=message.text,
                                        speaker=speaker,
                                        sample_rate=sample_rate
                                        )
        player = discord.FFmpegOpusAudio(audio_paths, **cls.ffmpeg_options)
        id = cls.message.guild.id
        cls.voice_clients[id].play(player)