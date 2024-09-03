from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import AuidoMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor

@discord_bot.bot.command(name='start_recording', help='This command starts recording')
async def start_recording(message: discord_bot.discord.ApplicationContext):
    smon = SongsMonitor.SongsMonitor(discord_bot.bot, message)

    mon = AuidoMonitorDiscord.AudioMonitorDiscord(message)

    await smon.join()
    await mon.monitor()

@discord_bot.bot.command(name='stop_recording', help='This command stops recording')
async def stop_recording(message: discord_bot.discord.ApplicationContext):

    mon = AuidoMonitorDiscord.AudioMonitorDiscord(message)
    await mon.stop()