from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import TextMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor

@discord_bot.bot.listen()
async def on_message(message):

    """
    This function is for taking messages from a chat
    """

    if message.author != discord_bot.bot.user:
        mmon = MessageMonitorDiscord.MessageMonitorDiscord(message)
        pmon = PictureMonitorDiscord.PictureMonitorDiscord(message)
        tmon = TextMonitorDiscord.TextMonitorDiscord(message)

        try:
            lowertext = message.content.lower()
            if lowertext.count('миса') >0:
                await tmon.join(message)
        except:
            pass
        photo = pmon.monitor()
        outstr = mmon.monitor()


        if photo != None:
            await message.channel.send(file=discord_bot.discord.File(photo))
        else:
            try:
                await tmon.monitor(outstr)
            except:
                try:
                    await message.channel.send(outstr)
                except:
                    pass



