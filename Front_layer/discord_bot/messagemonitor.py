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
        isCommand = False
        mmon = MessageMonitorDiscord.MessageMonitorDiscord(message)
        pmon = PictureMonitorDiscord.PictureMonitorDiscord(message)
        tmon = TextMonitorDiscord.TextMonitorDiscord(message)
        voice_client = None
        if (mmon.check(message.content)):
            isCommand = True
        else:
            lowertext = message.content.lower()
            if lowertext.count('миса') >0:
                voice_client = await tmon.join(message)


        photo = pmon.monitor()
        outstr = mmon.monitor()


        if photo != None:
            lowertext = message.content.lower()
            if lowertext.count('миса') >0:
                await message.channel.send(file=discord_bot.discord.File(photo))
        else:
            if outstr != '':
                if(isCommand):
                    await message.channel.send(outstr)
                else:
                    if(voice_client != None):
                        await tmon.monitor(outstr)
                    else:
                        await message.channel.send(outstr)




