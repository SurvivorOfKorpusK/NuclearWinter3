import subprocess

def packetsdownload():
    print("Устанавливаю необходимые для работы бота пакеты...")
    completed = subprocess.run(["powershell", "-Command", "pip install -r requirements.txt"], capture_output=True)
    return completed

flag = packetsdownload()
if flag:
    print("Все пакеты успешно установлены")
    api = str(input("Обратитесть к телеграм боту Bot Father, получите API Token для бота, введите его: "))
    with open("getapi.txt", 'w') as file:
        file.write(api)
    print("Инициализирован запуск бота")
    subprocess.run(["powershell", "-Command", "python chat.py"], capture_output=True)
else:
    print("Что-то пошло не так, попробуйте еще раз")