import telebot
from telebot import types
from telebot.types import BotCommand
from config import TOKEN
from datetime import datetime
import json

print(datetime.now())

data = {"users": []}
active_user = ""

try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except json.decoder.JSONDecodeError:
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

bot = telebot.TeleBot(TOKEN)
language = 'en'
user_name = ''
user_password = ''
task_name = ''
task_description = ''
task_priority = ''
task_term = ''
user_tasks = {}
commands = [
    BotCommand("start", "Start bot"),
    BotCommand("task", "Set task")
]

bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello!")
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton("English", callback_data="English"))
    inline_keyboard.add(types.InlineKeyboardButton("Русский", callback_data="Russian"))
    inline_keyboard.add(types.InlineKeyboardButton("Український", callback_data="Ukrainian"))
    bot.send_message(message.chat.id, "Chose your language.", reply_markup=inline_keyboard)

@bot.message_handler(commands=['task'])
def send_task(message):
    if language == 'en':
        bot.send_message(message.chat.id, "input task name: ")
    elif language == 'Русский':
        bot.send_message(message.chat.id, "Введите имя задачи: ")
    elif language == 'Український':
        bot.send_message(message.chat.id, "Введіть ім'я завдання: ")

    bot.register_next_step_handler(message, set_task_description)

@bot.message_handler(commands=['find'])
def find_task(message):
    if language == 'en':
        bot.send_message(message.chat.id, "input task name: ")
    elif language == 'Русский':
        bot.send_message(message.chat.id, "Введите имя задачи: ")
    elif language == 'Український':
        bot.send_message(message.chat.id, "Введіть ім'я завдання: ")

    bot.register_next_step_handler(message, start_find)

def start_find(message):
    find_name = message.text.strip()
    bot.send_message(message.chat.id, data["users"][active_user]["tasks"][find_name])

def set_task_description(message):
    global task_name
    task_name = message.text.strip()
    if language == 'en':
        bot.send_message(message.chat.id, "Input task description: ")

    elif language == 'Русский':
        bot.send_message(message.chat.id, "Введите описание задачи: ")

    elif language == 'Український':
        bot.send_message(message.chat.id, "Введіть опис завдання: ")


    bot.register_next_step_handler(message, set_task_priority)

def set_task_priority(message):
    global task_description
    task_description = message.text.strip()
    if language == 'en':
        bot.send_message(message.chat.id, "Input task priority: ")
    elif language == 'Русский':
        bot.send_message(message.chat.id, "Введите приоритет задачи: ")
    elif language == 'Український':
        bot.send_message(message.chat.id, "Введіть пріоритет завдання: ")

    bot.register_next_step_handler(message, set_task_term)

def set_task_term(message):
    global task_priority
    task_priority = message.text.strip()
    if language == 'en':
        bot.send_message(message.chat.id, "Input task term: ")
    elif language == 'Русский':
        bot.send_message(message.chat.id, "Введите срок задачи: ")
    elif language == 'Український':
        bot.send_message(message.chat.id, "Введіть термін завдання: ")

    bot.register_next_step_handler(message, send_task_term)

def send_task_term(message):
    global task_term, active_user
    task_term = message.text.strip()
    if language == 'en':
        bot.send_message(message.chat.id, "Task saved")
        bot.send_message(message.chat.id,
                         f"Name: {task_name}, Description: {task_description}, Priority: {task_priority}, Term: {task_term}")
    elif language == 'Русский':
        bot.send_message(message.chat.id, "Задача сохранена")
        bot.send_message(message.chat.id,
                         f"Имя: {task_name}, Описание: {task_description}, Приоритет: {task_priority}, Термин: {task_term}")
    elif language == 'Український':
        bot.send_message(message.chat.id, "Завдання збережено")
        bot.send_message(message.chat.id,
                         f"Ім'я: {task_name}, Опис: {task_description}, Пріоритет: {task_priority}, Термін: {task_term}")

    if active_user != "":
        data["users"][active_user]["tasks"][task_name] = [task_description, task_priority, task_term]
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    else:
        if language == 'en':
            bot.send_message(message.chat.id, "You don`t log in")
        elif language == 'Русский':
            bot.send_message(message.chat.id, "Вы не зашли в аккаунт")
        elif language == 'Український':
            bot.send_message(message.chat.id, "Ви не вішли у обліковий запис")

def register_name(message):
    global user_name
    user_name = message.text.strip()

    if language == 'en':
        bot.send_message(message.chat.id, "input password: ")
    elif language == 'Русский':
        bot.send_message(message.chat.id, "Введите пароль: ")
    elif language == 'Український':
        bot.send_message(message.chat.id, "Введіть пароль: ")

    bot.register_next_step_handler(message, register_password)

def register_password(message):
    global user_password, user_name, active_user
    user_password = message.text.strip()

    if user_name in data["users"] and user_password in data["users"][user_name]["password"]:
        if language == 'en':
            bot.send_message(message.chat.id, "You have logged into your account.")
        elif language == 'Русский':
            bot.send_message(message.chat.id, "Вы зашли в свой аккаунт")
        elif language == 'Український':
            bot.send_message(message.chat.id, "Ви зайшли до свого облікового запису")

        active_user = user_name
        task(message)
    else:
        data["users"][user_name]["password"] = user_password

        if language == 'en':
            bot.send_message(message.chat.id, "Your registered")
        elif language == 'Русский':
            bot.send_message(message.chat.id, "Вы зарегистрированы")
        elif language == 'Український':
            bot.send_message(message.chat.id, "Ви зарегиструвалися")

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

def task(message):
    expired = []
    for key in data["users"][user_name]["tasks"]:
        term = data["users"][user_name]["tasks"][key][-1]
        deadline = datetime.strptime(term, "%Y-%m-%d")
        if datetime.now() > deadline:
            if language == 'en':
                bot.send_message(message.chat.id, "Your train has left")
            elif language == 'Русский':
                bot.send_message(message.chat.id, "Ваш поезд уехал")
            elif language == 'Український':
                bot.send_message(message.chat.id, "Ваш поїзд поїхав без вас")

            expired.append(key)

        else:
            diff = deadline - datetime.now()
            if language == 'en':
                bot.send_message(message.chat.id, f"{diff.days} days left")
            elif language == 'Русский':
                bot.send_message(message.chat.id, f"Осталось {diff.days} дней")
            elif language == 'Український':
                bot.send_message(message.chat.id, f"Залишилось {diff.days} днів")

    for key in expired:
        del (data["users"][user_name]["tasks"][key])

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global language
    if call.data == "English":
        bot.send_message(call.message.chat.id, language)
    elif call.data == "Russian":
        language = "Русский"
        bot.send_message(call.message.chat.id, language)
    elif call.data == "Ukrainian":
        language = "Український"
        bot.send_message(call.message.chat.id, language)

    if language == 'en':
        bot.send_message(call.message.chat.id, "Input name: ")
    elif language == 'Русский':
        bot.send_message(call.message.chat.id, "Введите имя: ")
    elif language == 'Український':
        bot.send_message(call.message.chat.id, "Введіть ім'я: ")

    bot.register_next_step_handler(call.message, register_name)

if __name__ == '__main__':
    bot.polling(none_stop=True)
