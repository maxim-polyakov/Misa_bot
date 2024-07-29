from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import AudioMonitor

@telegram_bot.dp.message_handler(content_types=['voice'])
async def download_photo(message):
    file_info = await telegram_bot.boto.get_file(message.voice.file_id)
    await telegram_bot.boto.download_file(file_info.file_path, "audios/TmpAudioFile.wav")
    am = AudioMonitor.AudioMonitor()
    output = am.monitor()
    await telegram_bot.boto.send_message(message.chat.id, output, parse_mode='html')
