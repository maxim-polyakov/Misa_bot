from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors.MessageMonitorDiscord import MessageMonitorDiscord

@discord_bot.bot.listen()
async def on_message_EDA(message):
#
#
    if message.author != discord_bot.bot.user:
        mon = MessageMonitorDiscord.MessageMonitorDiscord(message)
        outstr = mon.monitor()
        try:
            await message.channel.send(outstr)
        except:
            pass

