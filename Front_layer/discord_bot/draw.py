from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Drawers import Drawer


@discord_bot.bot.slash_command(name='draw', description='Нарисовать что-нибудь')
async def draw(message, what_to_draw):
#
#
    await message.response.defer(ephemeral=True)
    draw = Drawer.Drawer(what_to_draw)
    outputder = draw.draw()
    photo = str(outputder)
    await message.channel.send(file=discord_bot.disnake.File(photo))
    await message.followup.send('Готово')


