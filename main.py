import telebot

import users

_bot = telebot.TeleBot('1898682710:AAGGjRKCbh3a2zPzylGSqQ_Se9x3xSCPBBM')
_users = users.Users()


@_bot.message_handler(commands=['start'])
def start_command(message):
    uid = message.from_user.id

    if not _users.isRegistered(uid):
        _users.registerUser(uid)
        _bot.reply_to(message, "Вы были зарегистрированы!")
    else:
        _bot.reply_to(message, "Для поиска необходимых материалов,\nвведите команду /search")


@_bot.message_handler(commands=['myrole'])
def myrole_command(message):
    uid = message.from_user.id

    if _users.isRegistered(uid):
        if _users.isAdmin(uid):
            _bot.reply_to(message, "Вы админ")
        else:
            _bot.reply_to(message, "Вы не админ")
    else:
        _bot.reply_to(message, "Вы не зарегистрированы. Как вы это сделали?")


_bot.polling()
