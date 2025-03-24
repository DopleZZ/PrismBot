import os
import sys
import telebot
import random
import signal

with open("./env", "r") as file:
    TOKEN = file.read()

bot = telebot.TeleBot("TOKEN", parse_mode=None)
lock_file = '/tmp/bot.lock'


if os.path.exists(lock_file):
    with open(lock_file, 'r') as f:
        old_pid = int(f.read().strip())
        try:
            os.kill(old_pid, signal.SIGTERM)
            print(f"Убит старый процесс с PID: {old_pid}")
        except ProcessLookupError:
            print("Предыдущий процесс не найден.")
        except PermissionError:
            print("Нет прав на завершение процесса.")
    os.remove(lock_file)

with open(lock_file, 'w') as f:
    f.write(str(os.getpid()))

@bot.message_handler(commands=['start'])
def zdarova(message):
    bot.send_message(message.chat.id, 'поприветкай мне тут, чучело ебанное. Мамаше своей привет напиши, порадуется, чмоноурод блять')

@bot.message_handler(content_types=['text'])
def handle_message(msg):
    
    if msg.from_user.username == "utilizator_forever":
        if random.random() < 0.1:
            print("Особое сообщение от @utilizator_forever!")
            bot.reply_to("хохол обнаружен", response)
    else:
        if random.random() < 0.01:
            print("пишем")
            response = random.choice(["кринж", "база", "истина", "хуета"])
            bot.reply_to(msg, response)
        else:
            print("пропускаем")
    
    if "вопрос" in msg.text:
        bot.reply_to(msg, random.choice(["да","нет"]))

print("Бот запущен...")
try:
    bot.polling(none_stop=True, interval=0)
finally:
    os.remove(lock_file)
    print("Бот остановлен")