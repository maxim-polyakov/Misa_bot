from Front_layer import discord_bot
import requests




@discord_bot.bot.slash_command(name="online", description="Показать онлайн сервера")
async def online(message):
    await message.response.defer(ephemeral=True)
    mbrs = message.guild.members
    online = len(list(filter(lambda x: x.status == discord_bot.disnake.Status.online, mbrs)))
    idle = len(list(filter(lambda x: x.status == discord_bot.disnake.Status.idle, mbrs)))
    offline = len(list(filter(lambda x: x.status == discord_bot.disnake.Status.offline, mbrs)))
    dnd = len(list(filter(lambda x: x.status == discord_bot.disnake.Status.dnd, mbrs)))
    out = 'онлайн: ' + str(online) + '\n' + 'отошёл: ' + str(idle) + '\n' + 'не беспокоить: ' + str(dnd) + '\n' + 'офлайн: ' + str(offline)
    await message.followup.send(out)


