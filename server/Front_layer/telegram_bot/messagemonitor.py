import os

from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorTelegram
from Core_layer.Bot_package.Classes.response_utils import (
    clean_command_response,
    extract_image_url,
    is_image_url,
    is_local_image_path,
)


@telegram_bot.dp.message_handler(content_types=['text'])
async def get_user_text(message):
    async def processing_large_messages(output):
        if len(output) > 4096:
            if not os.path.exists('txtfiles'):
                os.makedirs('txtfiles')
            with open('txtfiles/message.txt', 'w+', encoding='utf-8') as file:
                file.write(output)
            await telegram_bot.boto.send_document(
                message.chat.id, open('txtfiles/message.txt', 'r+', encoding='utf-8')
            )
        else:
            await telegram_bot.boto.send_message(message.chat.id, output)

    async def send_response_parts(output):
        parts = clean_command_response(output)
        if not parts and output and output.strip():
            parts = [output.strip()]
        for part in parts:
            if is_image_url(part):
                await telegram_bot.boto.send_photo(message.chat.id, photo=extract_image_url(part))
            elif is_local_image_path(part):
                await telegram_bot.boto.send_photo(message.chat.id, photo=open(part, 'rb'))
            else:
                await processing_large_messages(part)

    mon = MessageMonitorTelegram.MessageMonitorTelegram(
        telegram_bot.boto, message.from_user.username, message
    )
    output = mon.monitor()

    if output and output.strip():
        try:
            await send_response_parts(output)
        except Exception:
            pass
