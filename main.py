import os
import sys
import telebot
import random
import signal
import time

FACTS_FILE = 'facts.txt'

# Функции загрузки и добавления фактов

def load_facts():
    if not os.path.exists(FACTS_FILE):
        with open(FACTS_FILE, 'w') as f:
            pass
    with open(FACTS_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def add_fact(fact):
    with open(FACTS_FILE, 'a') as f:
        f.write(fact + '\n')

facts = load_facts()

with open("./env", "r") as file:
    TOKEN = file.read().strip()

bot = telebot.TeleBot(TOKEN, parse_mode=None)
lock_file = '/tmp/bot.lock'

if os.path.exists(lock_file):
    with open(lock_file, 'r') as f:
        old_pid = int(f.read().strip())
        try:
            os.kill(old_pid, signal.SIGTERM)
            print(f"Убит старый процесс с PID: {old_pid}")
        except ProcessLookupError:
            print("\u041f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0438\u0439 \u043f\u0440\u043e\u0446\u0435\u0441\u0441 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d.")
        except PermissionError:
            print("\u041d\u0435\u0442 \u043f\u0440\u0430\u0432 \u043d\u0430 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u0446\u0435\u0441\u0441\u0430.")
    os.remove(lock_file)

with open(lock_file, 'w') as f:
    f.write(str(os.getpid()))

@bot.message_handler(commands=['start'])
def zdarova(message):
    bot.send_message(message.chat.id, 'поприветкай мне тут, чучело ебанное. Мамаше своей привет напиши, порадуется, чмоноурод блять')

@bot.message_handler(commands=['факт'])
def fact_command(message):
    parts = message.text.split(' ', 1)
    if len(parts) > 1:
        add_fact(parts[1])
        bot.reply_to(message, 'зафиксировал')
    else:
        if facts:
            bot.reply_to(message, random.choice(facts))
        else:
            bot.reply_to(message, 'ниче не знаю')

@bot.message_handler(commands=['stop'])
def stop_command(message):
    if message.from_user.username == "vodka_kota":
        bot.reply_to(message, "Бот останавливается...")
        if os.path.exists(lock_file):
            os.remove(lock_file)
        sys.exit(0)
    else:
        bot.reply_to(message, "отъебись")

@bot.message_handler(content_types=['text'])
def handle_message(msg):
    if msg.text.lower().startswith('факт'):
        parts = msg.text.split(' ', 1)
        if len(parts) > 1:
            add_fact(parts[1])
            bot.reply_to(msg, 'зафиксировал')
        else:
            if facts:
                bot.reply_to(msg, random.choice(facts))
            else:
                bot.reply_to(msg, 'ниче не знаю')

    elif msg.from_user.username == "utilizator_forever":
        if random.random() < 0.1:
            print("Особое сообщение от @utilizator_forever!")
            bot.reply_to(msg, "хохол обнаружен")
    else:
        if random.random() < 0.01:
            print("пишем")
            response = random.choice(["кринж", "база", "истина", "хуета"])
            bot.reply_to(msg, response)
        else:
            print("пропускаем")

    if msg.text.lower().startswith("вопрос"):
        bot.reply_to(msg, random.choice(["да", "нет"]))

print("Бот запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5) 
    finally:
        if os.path.exists(lock_file):
            os.remove(lock_file)
        print("Бот остановлен, перезапуск...")
