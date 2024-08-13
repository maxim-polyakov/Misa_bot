from Front_layer import discord_bot
from Core_layer.Command_package.Classes.CommandActions import CommandAction

@discord_bot.bot.command(name='find', help='To play song')
async def find(message, subject):
    name = message.message.author.name
    if (name == 'seraphim8341'):
        cl = CommandAction.CommandAction(message, subject)
        out = cl.find()
        await message.channel.send(out)
    else:
        await message.channel.send('😊')