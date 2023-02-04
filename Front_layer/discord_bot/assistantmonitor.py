from Front_layer import discord_bot
from Core_layer.Bot_package import Token

@discord_bot.bot.command()
async def token(ctx, arg):
    if ctx.author != discord_bot.bot.user:
        if ctx.author.display_name == 'Seraphim' and ctx.author.discriminator == '8341':
            Token.TokenAdder.add_token(arg)
        else:
            await ctx.channel.send('😊')