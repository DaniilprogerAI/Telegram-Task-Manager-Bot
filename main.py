import telebot
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
language = 'en'
user_name = ''
user_password = ''

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello!")
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton("English", callback_data="English"))
    inline_keyboard.add(types.InlineKeyboardButton("Русский", callback_data="Russian"))
    inline_keyboard.add(types.InlineKeyboardButton("Український", callback_data="Ukrainian"))
    bot.send_message(message.chat.id, "Chose your language.", reply_markup=inline_keyboard)


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
    global user_password
    user_password = message.text.strip()

    if language == 'en':
        bot.send_message(message.chat.id, "Your registered")
    elif language == 'Русский':
        bot.send_message(message.chat.id, "Вы зарегистрированы")
    elif language == 'Український':
        bot.send_message(message.chat.id, "Ви зарегиструвалися")

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

    bot.register_next_step_handler(call.messageк, register_name)

bot.polling(none_stop=True)
