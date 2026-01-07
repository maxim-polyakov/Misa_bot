import os
import logging

from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import TextMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor


def is_file_path(response):
    if not isinstance(response, str):
        return False

    cleaned_path = response.strip().replace('\n', '')

    if os.path.exists(cleaned_path) and os.path.isfile(cleaned_path):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
        file_ext = os.path.splitext(cleaned_path)[1].lower()
        return file_ext in image_extensions

    return False

global flag
@discord_bot.bot.listen()
async def on_message(message):
#
#This function is for taking messages from a chat
    async def processing_large_messages(outstr):
        if (len(outstr) > 2000):
            if not os.path.exists('txtfiles'):
                os.makedirs('txtfiles')
            with open('txtfiles/message.txt', 'w+', encoding='utf-8') as file:
                file.write(outstr)
            await message.channel.send(file=discord_bot.disnake.File('txtfiles/message.txt'))
        else:
            await message.channel.send(outstr)
    if message.author != discord_bot.bot.user:
        isCommand = False
        mmon = MessageMonitorDiscord.MessageMonitorDiscord(discord_bot.bot, message.author.display_name, message)
        pmon = PictureMonitorDiscord.PictureMonitorDiscord(message)

        if (mmon.check(message.content, message.author.display_name)):
            isCommand = True

        photo = pmon.monitor()
        outstr = mmon.monitor()

        if photo != None:
            lowertext = message.content.lower()
            if lowertext.count('миса') > 0:
                await message.channel.send(file=discord_bot.disnake.File(photo))
        else:
            if outstr != '' or outstr != '\n':
                if(isCommand):
                    try:
                        if mmon.command_type() == '3':
                            outarr = outstr.split('|command|\n')
                            outarr = [word for word in outarr if word != '']
                            for el in outarr:
                                if (is_file_path(el)):
                                    await message.channel.send(file=discord_bot.disnake.File(el))
                                else:
                                    await processing_large_messages(el)
                        else:
                            outstr = outstr.replace('|command|\n', '')
                            await processing_large_messages(outstr)

                    except Exception as e:
                        logging.exception('The exception occurred in on_message ' + str(e))
                else:
                    try:
                        await message.channel.send(outstr)
                    except Exception as e:
                        logging.exception('The exception occurred in on_message ' + str(e))




