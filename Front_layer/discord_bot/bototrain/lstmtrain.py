from Front_layer import discord_bot
from Core_layer.Bot_package.Bototrainers import LSTMtrain

@discord_bot.bot.command()
async def LSTMemotionstrain_EDA(ctx, arg):
#
#
    try:
        if ctx.author != discord_bot.bot.user:
            if ctx.author.display_name == 'Seraphim' and ctx.author.discriminator == '8341':
                def train(message_text_array):
                    epochs = message_text_array.pop(0)
                    lt.emotionstrain(int(epochs))
                    return './models/binary/results_training/resultstraining_binary.png'
                lt = LSTMtrain.LSTMtrain()
                if (len(arg) > 0):
                    message_text_array = arg.split()
                    await ctx.channel.send(
                        file=discord_bot.discord.File(train(message_text_array)))
                else:
                    await ctx.channel.send(
                        file=discord_bot.discord.File(train(200)))
                    await ctx.channel.send('trained')
    except:
        await ctx.channel.send('😊')

@discord_bot.bot.command()
async def LSTMtrain_EDA(ctx, arg):
    try:
        if ctx.author != discord_bot.bot.user:
            if ctx.author.display_name == 'Seraphim' and ctx.author.discriminator == '8341':
                lt = LSTMtrain.LSTMtrain()
                if (len(arg) > 0):
                    message_text_array = arg
                    epochs = message_text_array.pop(0)
                    lt.hitrain(int(epochs))
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
                    if (message_text_array != []):
                        epochs = message_text_array.pop(0)
                    lt.thtrain(int(epochs))
                    await ctx.channel.send('thtrain')
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
                    if (message_text_array != []):
                        epochs = message_text_array.pop(0)
                    lt.businesstrain(int(epochs))
                    await ctx.channel.send('businesstrain')
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
                    if (message_text_array != []):
                        epochs = message_text_array.pop(0)
                    lt.weathertrain(int(epochs))
                    await ctx.channel.send('weathertrain')
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
                    if (message_text_array != []):
                        epochs = message_text_array.pop(0)
                    lt.trashtrain(int(epochs))
                    await ctx.channel.send('trashtrain')
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
                else:
                    message_text_array = arg
                    epochs = message_text_array.pop(0)
                    lt.hitrain(int(epochs))
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
                    if (message_text_array != []):
                        epochs = message_text_array.pop(0)
                    lt.thtrain(int(epochs))
                    await ctx.channel.send('thtrain')
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
                    if (message_text_array != []):
                        epochs = message_text_array.pop(0)
                    lt.businesstrain(int(epochs))
                    await ctx.channel.send('businesstrain')
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
                    if (message_text_array != []):
                        epochs = message_text_array.pop(0)
                    lt.weathertrain(int(epochs))
                    await ctx.channel.send('weathertrain')
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
                    if (message_text_array != []):
                        epochs = message_text_array.pop(0)
                    lt.trashtrain(int(epochs))
                    await ctx.channel.send('trashtrain')
                    await ctx.channel.send(
                        file=discord_bot.discord.File(
                            './models/binary/results_training/resultstraining_binary.png'))
    except:
        await ctx.channel.send('😊')
