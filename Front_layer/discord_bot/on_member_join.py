from Front_layer import discord_bot

@discord_bot.bot.event
async def on_member_join(member):
    channel = discord_bot.bot.get_channel(742732920099307571)
    embed=discord_bot.discord.Embed(title="Добро пожаловать!", description=f"{member.mention} Подюключился")
    await channel.send(embed=embed)