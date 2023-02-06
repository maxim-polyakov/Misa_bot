from Front_layer.telegram_bot import *
from aiogram import Bot, Dispatcher
from Core_layer.Bot_package import Token
from telebot import apihelper
# ______________________________________________________________________________

apihelper.proxy = {'https': 'socks5://telegram.vpn.net:55555'}

tkn = Token.Token()
df = tkn.get_token('select token from assistant_sets.tokens where botname = \'Misa\' and platformname = \'Telegram\'')
API_TOKEN = df['token'][0]
APP_HOST = '127.0.0.1'
APP_PORT = '9000'
boto = Bot(token=API_TOKEN)
dp = Dispatcher(boto)

