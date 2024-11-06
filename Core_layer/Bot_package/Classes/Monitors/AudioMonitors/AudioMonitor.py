import wave
import json
import logging
from vosk import Model, KaldiRecognizer, SetLogLevel
from Core_layer.Bot_package.Interfaces import IMonitor


class AudioMonitor(IMonitor.IMonitor):
    """

    This is a monitor for speach recognition

    """
    @classmethod
    def monitor(cls, file_path):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
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
            logging.info('The audiomonitor.monitor is done')
            return out
        except Exception as e:
            logging.exception(str('The exception in audiomonitor.monitor ' + str(e)))
