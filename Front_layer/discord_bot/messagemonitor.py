from Front_layer import discord_bot
from Core_layer.Bot_package import Monitors


@discord_bot.bot.listen()
async def on_message(message):
    if message.author != discord_bot.bot.user:
        mon = Monitors.MessageMonitorDiscord(message)
        outstr = mon.monitor()
        try:
            await message.channel.send(outstr)
        except:
            pass

