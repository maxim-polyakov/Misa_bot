import soundfile
import logging
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import AudioMonitor


class AudioMonitorTelegram(AudioMonitor.AudioMonitor):
    """

    It is a child of audio monitor for telegram

    """
    @classmethod
    def monitor(cls, filename):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            file_path = "audios/" + filename + ".wav"
            data, samplerate = soundfile.read(file_path)
            soundfile.write(file_path, data, samplerate)
            logging.info('The audiomonitortelegram.monitor is done')
            return super().monitor(file_path)
        except Exception as e:
            logging.exception(str('The exception in audiomonitortelegram.monitor ' + str(e)))