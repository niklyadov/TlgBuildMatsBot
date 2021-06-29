import telebot

bot = telebot.TeleBot('1898682710:AAGGjRKCbh3a2zPzylGSqQ_Se9x3xSCPBBM')


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Hello, world!")


bot.polling()
