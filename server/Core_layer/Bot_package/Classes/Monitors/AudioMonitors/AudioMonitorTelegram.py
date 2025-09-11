import soundfile
import logging
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import AudioMonitor


class AudioMonitorTelegram(AudioMonitor.AudioMonitor):
    """

    It is a child of audio monitor for telegram

    """
    @classmethod
    def monitor(cls, filename):
        # configure logging settings
        # set the logging level to info and specify the log file "misa.log" in write mode
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # construct the file path for the audio file
            file_path = "audios/" + filename + ".wav"
            # read the audio file using the soundfile library
            data, samplerate = soundfile.read(file_path)
            # write the audio file back (this operation seems redundant)
            soundfile.write(file_path, data, samplerate)
            # log that the monitoring process has completed successfully
            logging.info('The audiomonitortelegram.monitor process has completed successfully')
            # call the parent class's monitor method with the file path
            return super().monitor(file_path)
        except Exception as e:
            # log any exceptions that occur during the process
            logging.exception('The exception in audiomonitortelegram.monitor: ' + str(e))
