from Front_layer import telegram_bot

@telegram_bot.dp.message_handler(content_types=['photo'])
async def download_photo(message):
    await message.photo[-1].download(destination_dir=('/misa'))
