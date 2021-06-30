import telebot

import users

_bot = telebot.TeleBot('1898682710:AAGGjRKCbh3a2zPzylGSqQ_Se9x3xSCPBBM')
_users = users.Users()


@_bot.message_handler(commands=['start'])
def start_command(message):
    uid = message.from_user.id

    if not _users.is_registered(uid):
        _users.register_user(uid)
        _bot.reply_to(message, "Вы были зарегистрированы!")

    _bot.reply_to(message, "Для поиска необходимых материалов,\nвведите команду /search")


@_bot.message_handler(commands=['myrole'])
def my_role_command(message):
    uid = message.from_user.id

    if _users.is_registered(uid):
        if _users.is_admin(uid):
            _bot.reply_to(message, "Вы админ")
        else:
            _bot.reply_to(message, "Вы обычный пользователь")
    else:
        _bot.reply_to(message, "Вы не зарегистрированы. Как вы это сделали?")


_bot.polling()
