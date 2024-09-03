import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel
from Core_layer.Bot_package.Interfaces import IMonitor

class AudioMonitor(IMonitor.IMonitor):
    """

    Summary

    """
    @classmethod
    def monitor(cls, file_path):

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
                pass
            else:
                pass

        output = json.loads(rec.FinalResult())
        out = output["text"]
        return out