import os
from Front_layer import telegram_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorTelegram


@telegram_bot.dp.message_handler(content_types=['text'])
async def get_user_text(message):
#
#This function is for taking messages from a chat
    mon = MessageMonitorTelegram.MessageMonitorTelegram(telegram_bot.boto, message)
    output = mon.monitor()
    if(output != '' or output != '\n'):
        try:
            if message.text.lower().count('нарисуй') > 0:
                output = output.replace('\n', '')
                photo = str(output)
                await telegram_bot.boto.send_photo(message.chat.id, photo=open(photo, 'rb'))
            else:
                if (len(output) > 4096):
                    if not os.path.exists('txtfiles'):
                        os.makedirs('txtfiles')
                    with open('txtfiles/message.txt', 'w+', encoding='utf-8') as file:
                        file.write(output)
                    await telegram_bot.boto.send_document(message.chat.id, open('txtfiles/message.txt', 'r+', encoding='utf-8'))
                else:
                    await telegram_bot.boto.send_message(message.chat.id, output)
        except Exception as e:
            pass
