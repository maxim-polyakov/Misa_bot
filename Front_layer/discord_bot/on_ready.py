from asyncio import sleep
from Front_layer import discord_bot


@discord_bot.bot.event
async def on_ready():
#
#
    await discord_bot.bot.change_presence(
        status=discord_bot.disnake.Status.online,
        activity=discord_bot.disnake.CustomActivity("Смотрит за сервером"))
    await sleep(1)