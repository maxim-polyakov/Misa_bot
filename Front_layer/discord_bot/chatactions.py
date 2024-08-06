from Front_layer import discord_bot
import os
def remove_all_files(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

@discord_bot.bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    voice_channel = ctx.message.author.voice.channel
    await voice_channel.connect()

@discord_bot.bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    await voice_channel.disconnect()
