import os
from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor


def remove_all_files(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

@discord_bot.bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(message):
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.join()

@discord_bot.bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(message):
    sm = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    await sm.leave()
