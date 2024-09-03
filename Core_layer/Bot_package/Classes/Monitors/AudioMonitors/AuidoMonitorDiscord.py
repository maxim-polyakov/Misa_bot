import discord
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import AudioMonitor
from discord.sinks import WaveSink
import pydub
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json

class AudioMonitorDiscord(AudioMonitor.AudioMonitor):
    """

    Summary

    """

    def __init__(self, message):
        AudioMonitorDiscord.message = message

    async def __finished_callback(sink: WaveSink, channel: discord.TextChannel):
        mention_strs = []
        audio_segs: list[pydub.AudioSegment] = []
        files: list[discord.File] = []

        longest = pydub.AudioSegment.empty()

        file_path = ""

        for user_id, audio in sink.audio_data.items():
            mention_strs.append(f"<@{user_id}>")

            seg = pydub.AudioSegment.from_file(audio.file, format="wav")

            # Determine the longest audio segment
            if len(seg) > len(longest):
                audio_segs.append(longest)
                longest = seg
            else:
                audio_segs.append(seg)
            audio.file.seek(0)
            file = discord.File(audio.file, filename=f"{user_id}.wav")
            files.append(file)
            file_path = "audios/" + str(user_id) + ".wav"

        for seg in audio_segs:
            longest = longest.overlay(seg)
        longest.export(file_path, format="wav")
        await channel.send(
            f"Finished! Recorded audio for {', '.join(mention_strs)}.",
            files=files,
        )

    @classmethod
    async def stop(cls):
        """Stop the recording"""
        vc: discord.VoiceClient = cls.message.voice_client

        if not vc:
            return await cls.message.respond("There's no recording going on right now")

        vc.stop_recording()

        await cls.message.respond("The recording has stopped!")

    @classmethod
    async def monitor(cls):

        """Record the voice channel!"""
        voice = cls.message.author.voice

        if not voice:
            return await cls.message.respond("You're not in a vc right now")

        vc: discord.VoiceClient = cls.message.voice_client

        if not vc:
            return await cls.message.respond(
                "I'm not in a vc right now. Use `/join` to make me join!"
            )

        vc.start_recording(
            WaveSink(),
            cls.__finished_callback,
            cls.message.channel,
            sync_start=True,  # WARNING: This feature is very unstable and may break at any time.
        )