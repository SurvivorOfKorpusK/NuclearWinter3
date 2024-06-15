import telebot
import os
from ultralytics import YOLO


bot = telebot.TeleBot("7250952575:AAElJxVJINJdT3elaUYfFvBNuDTatfxea6A")
model = YOLO("model/yolov8n.pt")
model = YOLO("model/train7/weights/best.pt")


# @bot.message_handler(content_types=['document'])
# def handle_document(message):
#     file_info = bot.get_file(message.document.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#     file_path = os.path.join("userimgs", message.document.file_name)
#     with open(file_path, 'wb') as new_file:
#         new_file.write(downloaded_file)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Отправьте мне фотографию сварочного шва, и в ответе я верну фотографию, где будут отмечены дефекты")


@bot.message_handler(commands=['legend'])
def send_welcome(message):
    bot.reply_to(message,
                 "-Прилегающие дефекты - adj\n-Дефекты целостности - int\n-Дефекты геометрии - geo\n-Дефекты постобработки - pro\n-Дефекты невыполнения - non")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join("userimgs", f"{file_id}.jpg")
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    if RogueAI(file_path):
        with open("result.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove(os.path.join("userimgs", f"{file_id}.jpg"))
        os.remove("result.png")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я ОБРАБАТЫВАЮ ФОТОРАФИИ ШВОВ.")


def RogueAI(target):
    results = model(target)

    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs # display to screen
        result.save(filename="result.png")  # save to dis

    return True


bot.polling()
