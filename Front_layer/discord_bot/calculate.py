from Front_layer import discord_bot
from Core_layer.Command_package.Classes.CommandActions import CommandAction


@discord_bot.bot.slash_command(name='calculate', description='Вычислить производную')
async def calculate(message, fsubject = 'x', ssubject = 'x'):
#
#
    await message.channel.send('Выполняется команда')
    name = message.message.author.name
    subject = fsubject + ' ' + ssubject
    calc = CommandAction.CommandAction(message, subject)
    outputder = calc.eighth()
    await message.channel.send(outputder)
    await message.channel.send('Готово')