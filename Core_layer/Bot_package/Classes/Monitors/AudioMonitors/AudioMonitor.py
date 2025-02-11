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
        # this class method processes an audio file and converts speech to text
        # configure logging to store logs in "misa.log" file
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # open the audio file in read mode
            wf = wave.open(file_path, "rb")
            # initialize the speech recognition model
            model = Model(model_name="vosk-model-ru-0.42")
            # create a recognizer object with the model and sample rate of the audio file
            rec = KaldiRecognizer(model, wf.getframerate())
            # enable word-level and partial word recognition
            rec.SetWords(True)
            rec.SetPartialWords(True)
            # process the audio file in chunks
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    # stop if there is no more data
                    break
                # process the audio data
                if rec.AcceptWaveform(data):
                    # finalized recognition result
                    pass
                else:
                    # partial recognition result
                    pass
            # get the final recognition result and parse it as json
            output = json.loads(rec.FinalResult())
            out = output["text"]
            # log that the monitoring process is complete
            logging.info('The audiomonitor.monitor process is completed successfully')
            return out
        except Exception as e:
            # log any exceptions that occur during processing
            logging.exception('The exception occurred in audiomonitor.monitor: ' + str(e))
