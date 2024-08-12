from Front_layer import discord_bot
from asyncio import sleep #не забываем


@discord_bot.bot.event
async def on_ready():
    while True:
        await discord_bot.bot.change_presence(
            status=discord_bot.discord.Status.online,
            activity=discord_bot.discord.CustomActivity("Смотрит за сервером"))
        await sleep(15)