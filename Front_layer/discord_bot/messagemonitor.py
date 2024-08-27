from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitorDiscord


@discord_bot.bot.listen()
async def on_message(message):

    """
    This function is for taking messages from a chat
    """

    if message.author != discord_bot.bot.user:
        mmon = MessageMonitorDiscord.MessageMonitorDiscord(message)
        pmon = PictureMonitorDiscord.PictureMonitorDiscord(message)
        photo = pmon.monitor()
        outstr = mmon.monitor()

        try:
            if photo != None:
                await message.channel.send(file=discord_bot.discord.File(photo))
            await message.channel.send(outstr)
        except:
            pass

