import disnake
import wave
import json
import pydub
import logging
from discord.sinks import WaveSink
from vosk import Model, KaldiRecognizer, SetLogLevel
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import AudioMonitor


class AudioMonitorDiscord(AudioMonitor.AudioMonitor):
    """

    It is a child of audio monitor for discord

    """
    message = None
    def __init__(self, message):
        AudioMonitorDiscord.message = message
    @classmethod
    async def __finished_callback(sink: WaveSink, channel: discord.TextChannel):
        # finishing callback of audios
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # list to store user mentions
            mention_strs = []
            # list to store audio segments
            audio_segs: list[pydub.AudioSegment] = []
            # list to store discord file objects
            files: list[disnake.File] = []
            # variable to store the longest audio segment
            longest = pydub.AudioSegment.empty()
            # variable to store the final file path
            file_path = ""
            # iterate through recorded audio data
            for user_id, audio in sink.audio_data.items():
                mention_strs.append(f"<@{user_id}>")
                # load the audio file as a pydub audiosegment
                seg = pydub.AudioSegment.from_file(audio.file, format="wav")
                # determine the longest audio segment
                if len(seg) > len(longest):
                    audio_segs.append(longest)
                    longest = seg
                else:
                    audio_segs.append(seg)
                # reset file pointer and create a discord file object
                audio.file.seek(0)
                file = disnake.File(audio.file, filename=f"{user_id}.wav")
                files.append(file)
                # define the file path for saving the audio
                file_path = "audios/" + str(user_id) + ".wav"
            # overlay all audio segments onto the longest one
            for seg in audio_segs:
                longest = longest.overlay(seg)
            # export the final mixed audio file
            longest.export(file_path, format="wav")
            # send the recorded audio files to the discord channel
            await channel.send(
                f"Finished! Recorded audio for {', '.join(mention_strs)}.",
                files=files,
            )
            # log successful completion of the function
            logging.info('The audiomonitordiscord.__finished_callback process has completed successfully')
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception in audiomonitordiscord.__finished_callback: ' + str(e))

    @classmethod
    async def stop(cls):
        # stop the recording
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # get the voice client from the message context
            vc: disnake.VoiceClient = cls.message.guild.voice_client

            # check if there is an active voice client
            if not vc:
                return await cls.message.followup.send(
                    "Я не в войс канале сейчас"
                )
            # stop the recording
            vc.stop_recording()
            # notify the user that the recording has stopped
            await cls.message.followup.send("Запись была остановлена")
            # log the successful stop of the recording
            logging.info('The audiomonitordiscord.stop process has completed successfully')
        except Exception as e:
            # log any exceptions that occur during the stop process
            logging.exception('The exception occurred in audiomonitordiscord.stop: ' + str(e))


    @classmethod
    async def monitor(cls):
        # record the voice channel
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # get the voice state of the message author
            voice = cls.message.author.voice
            # check if the user is in a voice channel
            if not voice:
                return await cls.message.followup.send("Вы не в войс канале сейчас")
            # get the bot's voice client
            vc: disnake.VoiceClient = cls.message.guild.voice_client
            # check if the bot is connected to a voice channel
            if not vc:
                return await cls.message.followup.send(
                    "Я не в войс канале сейчас"
                )
            # start recording the voice channel
            vc.start_recording(
                WaveSink(),  # define the recording format
                cls.__finished_callback,  # callback function when recording ends
                cls.message.channel,  # the channel where the bot will send the recording
                sync_start=True,  # WARNING: This feature is very unstable and may break at any time.
            )
            # log that the monitoring function has started successfully
            logging.info('The audiomonitordiscord.monitor process has completed successfully')
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in audiomonitordiscord.monitor: ' + str(e))
