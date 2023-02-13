from Front_layer import discord_bot
from Core_layer.Bot_package.Monitors import Classes

@discord_bot.bot.listen()
async def on_message(message):
    if message.author != discord_bot.bot.user:
        mon = Classes.MessageMonitorDiscord(message)
        outstr = mon.monitor()
        try:
            await message.channel.send(outstr)
        except:
            pass

