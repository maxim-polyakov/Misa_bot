from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import AuidoMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor


@discord_bot.bot.slash_command(name='start_recording', description='Включить записывание')
async def start_recording(message):
#
#
    await message.response.defer(ephemeral=True)
    smon = SongsMonitor.SongsMonitor(discord_bot.bot, message)
    mon = AuidoMonitorDiscord.AudioMonitorDiscord(message)
    await smon.join()
    await mon.monitor()
    await message.followup.send('Готово')
@discord_bot.bot.slash_command(name='stop_recording', description='Остановить записывание')
async def stop_recording(message):
#
#
    await message.response.defer(ephemeral=True)
    mon = AuidoMonitorDiscord.AudioMonitorDiscord(message)
    await mon.stop()
    await message.followup.send('Готово')