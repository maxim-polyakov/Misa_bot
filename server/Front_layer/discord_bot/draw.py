import io
import requests
from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Drawers import Drawer


@discord_bot.bot.slash_command(name='draw', description='Нарисовать что-нибудь')
async def draw(message, what_to_draw):
    await message.response.defer(ephemeral=True)
    draw = Drawer.Drawer(what_to_draw)
    outputder = draw.draw()
    if not outputder:
        await message.followup.send('Не удалось сгенерировать изображение')
        return
    # S3 URL или локальный путь
    if str(outputder).startswith('http'):
        r = requests.get(outputder)
        r.raise_for_status()
        await message.followup.send(file=discord_bot.disnake.File(io.BytesIO(r.content), filename='image.png'))
    else:
        await message.followup.send(file=discord_bot.disnake.File(outputder))


