from Front_layer import discord_bot
from Core_layer.Command_package.Classes.CommandActions import CommandAction


@discord_bot.bot.slash_command(name='calculate', description='Вычислить производную')
async def calculate(message, fsubject = 'x', ssubject = 'x'):
#
#
    name = message.message.author.name
    if (name == 'seraphim8341'):
        subject = fsubject + ' ' + ssubject
        calc = CommandAction.CommandAction(message, subject)
        outputder = calc.eighth()
        await message.channel.send(outputder)
    else:
        await message.channel.send('😊')