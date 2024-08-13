from Front_layer import discord_bot
from Core_layer.Command_package.Classes.CommandActions import CommandAction

@discord_bot.bot.command(name='weather', help='To play song')
async def weather(message, city1 = '', city2 = ''):
    name = message.message.author.name
    if (name == 'seraphim8341'):
        if city2 != '':
            city = city1 + ' ' + city2
        else:
            city = city1

        cl = CommandAction.CommandAction(message, city)
        out = cl.weather()
        await message.channel.send(out)
    else:
        await message.channel.send('😊')