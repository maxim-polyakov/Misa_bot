import os
from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorTelegram

def is_file_path(response):
    if not isinstance(response, str):
        return False

    cleaned_path = response.strip().replace('\n', '')

    if os.path.exists(cleaned_path) and os.path.isfile(cleaned_path):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
        file_ext = os.path.splitext(cleaned_path)[1].lower()
        return file_ext in image_extensions

    return False

@telegram_bot.dp.message_handler(content_types=['text'])
async def get_user_text(message):
#
#This function is for taking messages from a chat
    async def processing_large_messages(output):
        if (len(output) > 4096):
            if not os.path.exists('txtfiles'):
                os.makedirs('txtfiles')
            with open('txtfiles/message.txt', 'w+', encoding='utf-8') as file:
                file.write(output)
            await telegram_bot.boto.send_document(message.chat.id, open('txtfiles/message.txt', 'r+', encoding='utf-8'))
        else:
            await telegram_bot.boto.send_message(message.chat.id, output)
    mon = MessageMonitorTelegram.MessageMonitorTelegram(telegram_bot.boto, message.from_user.username, message)
    output = mon.monitor()
    if(output != '' or output != '\n'):
        try:
            if mon.command_type() == '3':
                outarr = output.split('|command|\n')
                outarr = [word for word in outarr if word != '']
                for el in outarr:
                    if (is_file_path(el)):
                        photo = str(el)
                        await telegram_bot.boto.send_photo(message.chat.id, photo=open(photo, 'rb'))
                    else:
                        await processing_large_messages(el)
            else:
                output = output.replace('|command|\n', '')
                await processing_large_messages(output)

        except Exception as e:
            pass
