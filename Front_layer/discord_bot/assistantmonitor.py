from Front_layer import discord_bot
from Core_layer.Bot_package import TokenAdder

@discord_bot.bot.command()
async def token(ctx, arg):
    if ctx.author != discord_bot.bot.user:
        if ctx.author.display_name == 'Seraphim' and ctx.author.discriminator == '8341':
            TokenAdder.TokenAdder.add_token(arg)
        else:
            await ctx.channel.send('😊')