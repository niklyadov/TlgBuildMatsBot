import telebot
import BestFinder
import Settings

import Users

_bot = telebot.TeleBot('1898682710:AAGGjRKCbh3a2zPzylGSqQ_Se9x3xSCPBBM')
_users = Users.Users()


@_bot.message_handler(commands=['start'])
def start_command(message):
    uid = message.from_user.id

    if not _users.is_registered(uid):
        _users.register_user(uid)
        _bot.reply_to(message, "Вы были зарегистрированы!")

    _bot.reply_to(message, "Для поиска необходимых материалов,\nвведите команду '/search [запрос]")


@_bot.message_handler(regexp="/search$")
def search_command(message):
    _bot.reply_to(message, "Для поиска необходимых материалов,\nвведите команду '/search [запрос]")


# TODO - сделать нормальный вывод
@_bot.message_handler(regexp="/search [а-яА-Я \-]*")
def search_word_command(message):
    uid = message.from_user.id
    settings = Settings.Settings.get_settings(uid)
    bf = BestFinder.BestFinder(settings[0], settings[1])
    top = bf.find_best(message.text[8:])
    msg = ""
    if len(top) == 0:
        _bot.reply_to(message, "Ничего не найдено")
    else:
        for item in top:
            msg += "{}:\nЦена: {} за {}\nДоступно в {}\nРейтинг: {}\n{}\n\n".format(item.name, item.price, item.per, item.available_at, item.rating, item.url)

        _bot.reply_to(message, msg)


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


@_bot.message_handler(commands=['test'])
def test(message):
    stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
    crossIcon = u"\u274C"
    markup = telebot.types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        markup.add(telebot.types.InlineKeyboardButton(text=value,
                                              callback_data="['value', '" + value + "', '" + key + "']"),
                   telebot.types.InlineKeyboardButton(text=crossIcon,
                                              callback_data="['key', '" + key + "']"))
    _bot.send_message(chat_id=message.chat.id,
                     text="Here are the values of stringList",
                     reply_markup=markup,
                     parse_mode='HTML')

_bot.polling()
