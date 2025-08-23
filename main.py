import telebot

bot = telebot.TeleBot('8150059268:AAHYIbiwsPT83w69ihY3Fh5YQ1LNPwf6bjY')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello!")
    bot.send_message(message.chat.id, "Chose your language.")