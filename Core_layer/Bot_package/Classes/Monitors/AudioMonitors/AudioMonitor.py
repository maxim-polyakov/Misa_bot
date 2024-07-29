import wave
import sys
import soundfile
import json

from vosk import Model, KaldiRecognizer, SetLogLevel
from Core_layer.Bot_package.Interfaces import IMonitor

class AudioMonitor(IMonitor.IMonitor):
    """

    Summary

    """
    @classmethod
    def monitor(cls):

        file_path = "audios/123.wav"
        data, samplerate = soundfile.read(file_path)
        soundfile.write(file_path, data, samplerate)

        wf = wave.open(file_path, "rb")

        # You can also init model by name or with a folder path
        model = Model(model_name="vosk-model-ru-0.42")
        # model = Model("models/en")

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        rec.SetPartialWords(True)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                print(rec.PartialResult())

        output = json.loads(rec.FinalResult())
        out = output["text"]
        return out