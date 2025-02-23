from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Weather import Weather


@discord_bot.bot.slash_command(name='weather', descriprion='Предсказание погоды')
async def weather(message, city1 = '', city2 = ''):
#
#
    await message.response.defer(ephemeral=True)
    name = message.message.author.name
    if city2 != '':
        city = city1 + ' ' + city2
    else:
        city = city1
    cl = Weather.Weather(message_text=city)
    out = cl.predict()
    await message.followup.send(out)
