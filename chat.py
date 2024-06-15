import telebot
import os
from ultralytics import YOLO


bot = telebot.TeleBot("7250952575:AAElJxVJINJdT3elaUYfFvBNuDTatfxea6A")
model = YOLO("model/yolov8n.pt")
model = YOLO("model/ourModel/best.pt")

pictext = ['.jpg', 'jpeg', '.png']
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    if str(file_info.file_path).split("/")[-1][-4:].lower() not in pictext:
        bot.reply_to(message,
                     "К сожалению, я умею работать только с фотографиями, пожалуйста отправьте мне фотографию с расширением jpeg или png")
    else:
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = os.path.join("userimgs", message.document.file_name)
        print(file_path)
        filename = file_path.split("\\")[-1]
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        resultname = RogueAI(file_path, message.id)
        if resultname:
            with open(resultname, "rb") as photo:
                bot.send_photo(message.chat.id, photo)
            os.remove(os.path.join("userimgs", filename))
            os.remove(resultname)
        else:
            os.remove(os.path.join("userimgs", filename))
            bot.reply_to(message,
                         "На данном фото дефектов не обнаружено")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 "Отправьте мне фотографию сварочного шва, и в ответе я верну фотографию, где будут отмечены дефекты")


@bot.message_handler(commands=['legend'])
def legend(message):
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
    resultname = RogueAI(file_path, message.id)
    if resultname:
        with open(resultname, "rb") as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove(os.path.join("userimgs", f"{file_id}.jpg"))
        os.remove(resultname)
    else:
        os.remove(os.path.join("userimgs", f"{file_id}.jpg"))
        bot.reply_to(message,
                     "На данном фото дефектов не обнаружено")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я ОБРАБАТЫВАЮ ФОТОРАФИИ ШВОВ.")


def RogueAI(target, id):
    results = model(target)
    newfilename = target.split("\\")[-1].split(".jpg")[0] + str(id) + ".png"

    for result in results:
        boxes = result.boxes
        if len(boxes.cls) < 1:
            return ""
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs
        obb = result.obb
        result.save(filename=newfilename)

    return newfilename


bot.polling()
