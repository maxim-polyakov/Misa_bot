from Front_layer import discord_bot
from Core_layer.Bot_package.Classes.Weather import Weather


@discord_bot.bot.slash_command(name='weather', help='Предсказание погоды')
async def weather(message, city1 = '', city2 = ''):
#
#
    name = message.message.author.name
    if (name == 'seraphim8341'):
        if city2 != '':
            city = city1 + ' ' + city2
        else:
            city = city1

        cl = Weather.Weather(message_text=city)
        out = cl.predict()
        await message.channel.send(out)
    else:
        await message.channel.send('😊')