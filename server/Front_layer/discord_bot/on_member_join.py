from Front_layer import discord_bot


@discord_bot.bot.event
async def on_member_join(member):
#
#
    channel = discord_bot.bot.get_channel(725486017670545429)
    embed=discord_bot.disnake.Embed(title="добро пожаловать!", description=f"{member.mention} подюключился")
    await channel.send(embed=embed)