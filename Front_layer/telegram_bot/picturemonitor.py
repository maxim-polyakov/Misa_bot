from Front_layer import telegram_bot

@telegram_bot.dp.message_handler(content_types=['photo'])
async def photo(message):
   idphoto = message.photo[0].file_id

   await telegram_bot.boto.send_photo(message.chat.id, idphoto)