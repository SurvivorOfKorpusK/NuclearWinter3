import telebot
import os

bot = telebot.TeleBot("7250952575:AAElJxVJINJdT3elaUYfFvBNuDTatfxea6A")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join("userimgs", message.document.file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join("userimgs", f"{file_id}.jpg")
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    with open(os.path.join("userimgs", "6f46de0337d3ec4b414f1aee92a9cfdb.jpg"), 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я ОБРАБАТЫВАЮ ФОТОРАФИИ ШВОВ.")


bot.polling()
