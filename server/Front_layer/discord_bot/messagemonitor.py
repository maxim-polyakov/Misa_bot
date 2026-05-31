import os
import logging

from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitorDiscord


def is_file_path(response):
    if not isinstance(response, str):
        return False

    cleaned_path = response.strip().replace('\n', '')

    if os.path.exists(cleaned_path) and os.path.isfile(cleaned_path):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
        file_ext = os.path.splitext(cleaned_path)[1].lower()
        return file_ext in image_extensions

    return False


@discord_bot.bot.listen()
async def on_message(message):
    async def processing_large_messages(outstr):
        if len(outstr) > 2000:
            if not os.path.exists('txtfiles'):
                os.makedirs('txtfiles')
            with open('txtfiles/message.txt', 'w+', encoding='utf-8') as file:
                file.write(outstr)
            await message.channel.send(file=discord_bot.disnake.File('txtfiles/message.txt'))
        else:
            await message.channel.send(outstr)

    if message.author == discord_bot.bot.user:
        return

    mmon = MessageMonitorDiscord.MessageMonitorDiscord(
        discord_bot.bot, message.author.display_name, message
    )
    pmon = PictureMonitorDiscord.PictureMonitorDiscord(message)

    photo = pmon.monitor()
    outstr = mmon.monitor()

    if photo is not None:
        lowertext = message.content.lower()
        if lowertext.count('миса') > 0 or lowertext.count('misa') > 0:
            await message.channel.send(file=discord_bot.disnake.File(photo))
    elif outstr and outstr.strip():
        try:
            await processing_large_messages(outstr)
        except Exception as e:
            logging.exception('The exception occurred in on_message ' + str(e))
