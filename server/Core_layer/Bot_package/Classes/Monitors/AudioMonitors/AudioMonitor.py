import wave
import json
import logging
from vosk import Model, KaldiRecognizer, SetLogLevel
from Core_layer.Bot_package.Interfaces import IMonitor
from openai import OpenAI

class AudioMonitor(IMonitor.IMonitor):
    """

    This is a monitor for speach recognition

    """
    @classmethod
    def monitor(cls, file_path):
        # this class method processes an audio file and converts speech to text
        # configure logging to store logs in "misa.log" file
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # retrieving api tokens from the database
            fdf = cls.__dbc.get_data(
                'select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Gpt\'')
            sdf = cls.__dbc.get_data(
                'select token from assistant_sets.projects where botname = \'Misa\' and platformname = \'Gpt\'')
            tdf = cls.__dbc.get_data(
                'select token from assistant_sets.organizations where botname = \'Misa\' and platformname = \'Gpt\'')
            # extracting api keys from the retrieved data
            OPENAI_API_KEY = fdf['token'][0]
            OPENAI_API_PROJECT = sdf['token'][0]
            OPENAI_API_ORG = tdf['token'][0]
            # initializing openai client with api credentials
            client = OpenAI(
                api_key=OPENAI_API_KEY,
                organization=OPENAI_API_ORG,
                project=OPENAI_API_PROJECT,
            )

            # Transcribing an audio file with Whisper
            with open(file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="ru"
                )
            transcribed_text = transcription.text
            logging.info('The audiomonitor.monitor process has completed successfully')
            return transcribed_text
        except Exception as e:
            # log any exceptions that occur during processing
            logging.exception('The exception occurred in audiomonitor.monitor: ' + str(e))
