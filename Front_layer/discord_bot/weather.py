from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Weather import Weather


@discord_bot.bot.slash_command(name='weather', description='Предсказание погоды')
async def weather(message, city):
#
#
    await message.response.defer(ephemeral=True)
    cl = Weather.Weather(message_text=city)
    out = cl.predict()
    await message.followup.send(out.lower())
