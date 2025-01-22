import os
from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Monitors.MessageMonitors import MessageMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.PictureMonitors import PictureMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import TextMonitorDiscord
from Core_layer.Bot_package.Classes.Monitors.AudioMonitors import SongsMonitor


global flag
@discord_bot.bot.listen()
async def on_message(message):
#
#This function is for taking messages from a chat
    if message.author != discord_bot.bot.user:
        isCommand = False
        mmon = MessageMonitorDiscord.MessageMonitorDiscord(discord_bot.bot, message)
        pmon = PictureMonitorDiscord.PictureMonitorDiscord(message)
        tmon = TextMonitorDiscord.TextMonitorDiscord(message)
        voice_client = None
        if (mmon.check(message.content)):
            isCommand = True
        else:
            lowertext = message.content.lower()
            if lowertext.count('миса') > 0:
                voice_client = await tmon.join(message)
                flag = True


        photo = pmon.monitor()
        outstr = mmon.monitor()


        if photo != None:
            lowertext = message.content.lower()
            if lowertext.count('миса') > 0:
                await message.channel.send(file=discord_bot.discord.File(photo))
        else:
            if outstr != '' or outstr != '\n':
                if(isCommand):
                    try:
                        if message.content.lower().count('нарисуй') > 0:
                            outstr = outstr.replace('\n', '')
                            await message.channel.send(file=discord_bot.discord.File(outstr))
                        else:
                            if(len(outstr) > 2000):
                                if not os.path.exists('txtfiles'):
                                    os.makedirs('txtfiles')
                                with open('txtfiles/message.txt', 'w+', encoding='utf-8') as file:
                                    file.write(outstr)
                                await message.channel.send(file=discord_bot.discord.File('txtfiles/message.txt'))
                            else:
                                await message.channel.send(outstr)
                    except Exception as e:
                        pass
                else:
                    if(voice_client != None or flag):
                        await tmon.monitor(outstr)
                    else:
                        try:
                            await message.channel.send(outstr)
                        except Exception as e:
                            pass




