from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import AudioMonitorTelegram
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorVoice


@telegram_bot.dp.message_handler(content_types=['voice'])
async def download_photo(message):
#
#
    file_info = await telegram_bot.boto.get_file(message.voice.file_id)
    filename = "TmpAudiofile"
    await telegram_bot.boto.download_file(file_info.file_path, "audios/" + filename + ".wav")
    am = AudioMonitorTelegram.AudioMonitorTelegram()
    output = am.monitor(filename)
    #await telegram_bot.boto.send_message(message.chat.id, output, parse_mode='html')
    mon = MessageMonitorVoice.MessageMonitorVoice(telegram_bot.boto, output)
    out = mon.monitor()
    await telegram_bot.boto.send_message(message.chat.id, out)