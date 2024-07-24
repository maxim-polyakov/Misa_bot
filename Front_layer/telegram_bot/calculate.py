from Front_layer import telegram_bot
from Core_layer.API_package.Classes.Calculators import SympyCalculator


@telegram_bot.dp.message_handler(commands=['calculate'])
async def get_user_text(message):
    #
    #
    if (message.chat.username == 'The_Baxic'):
        inpt = message.text.replace('/calculate ', '')
        calc = SympyCalculator.SympyCalculator()
        input_arr = inpt.split(' ')
        outputder = calc.deravative(input_arr[0], input_arr[1])
        outputint = calc.integrate(input_arr[0], input_arr[1])
        await telegram_bot.boto.send_message(message.chat.id, outputder, parse_mode='html')
        await telegram_bot.boto.send_message(message.chat.id, outputint, parse_mode='html')
    else:
        await telegram_bot.boto.send_message(message.chat.id, '😊', parse_mode='html')
