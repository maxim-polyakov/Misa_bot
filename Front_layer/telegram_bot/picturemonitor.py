from Front_layer import telegram_bot

@telegram_bot.dp.message_handler(content_types=['photo'])
async def photo(message):
    file = telegram_bot.boto.getFile(message.photo.file_id)
    print ("file_id: " + str(message.photo.file_id))
    file.download('image.jpg')