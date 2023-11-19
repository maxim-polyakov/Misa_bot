from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorDiscord

@discord_bot.bot.listen()
async def on_message(message):

    """
    This finction is for taking messsages from a chat
    """

    if message.author != discord_bot.bot.user:
        mon = MessageMonitorDiscord.MessageMonitorDiscord(message)
        outstr = mon.monitor()
        try:
            await message.channel.send(outstr)
        except:
            pass

