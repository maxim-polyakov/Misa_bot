from Front_layer.telegram_bot import *
from aiogram import Bot, Dispatcher

# ______________________________________________________________________________
API_TOKEN = '5770877310:AAEUujAIzyDrTTVhAauSuc3E2ukFhU9hrr0'
APP_HOST = '127.0.0.1'
APP_PORT = '9000'
boto = Bot(token=API_TOKEN)
dp = Dispatcher(boto)

