import soundfile
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import AudioMonitor

class AudioMonitorTelegram(AudioMonitor.AudioMonitor):
    """

    Summary

    """
    @classmethod
    def monitor(cls, filename):

        file_path = "audios/" + filename + ".wav"
        data, samplerate = soundfile.read(file_path)
        soundfile.write(file_path, data, samplerate)

        return super().monitor(file_path)