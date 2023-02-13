from Front_layer import discord_bot
from Core_layer.Bot_package.DataCleaners import Classes

@discord_bot.bot.command()
async def clean(ctx, arg):
    if ctx.author != discord_bot.bot.user:
        if ctx.author.display_name == 'Seraphim' and ctx.author.discriminator == '8341':
            cl = Classes.MisaMemoryCleater(arg)
            cl.clean()
            await ctx.channel.send('cleaned')
        else:
            await ctx.channel.send('😊')
