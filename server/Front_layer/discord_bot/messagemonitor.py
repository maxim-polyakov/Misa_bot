import io
import os
import logging

import requests

from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitorDiscord
from Core_layer.Bot_package.Classes.response_utils import (
    clean_command_response,
    extract_image_url,
    is_image_url,
    is_local_image_path,
)


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

    async def send_response_parts(outstr):
        parts = clean_command_response(outstr)
        if not parts and outstr and outstr.strip():
            parts = [outstr.strip()]
        for part in parts:
            if is_image_url(part):
                r = requests.get(extract_image_url(part), timeout=30)
                r.raise_for_status()
                await message.channel.send(
                    file=discord_bot.disnake.File(io.BytesIO(r.content), filename='image.png')
                )
            elif is_local_image_path(part):
                await message.channel.send(file=discord_bot.disnake.File(part))
            else:
                await processing_large_messages(part)

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
            await send_response_parts(outstr)
        except Exception as e:
            logging.exception('The exception occurred in on_message ' + str(e))
