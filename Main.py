import telebot
import BestFinder
import Favourites
import Settings
import Requests

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


# TODO - сделать нормальный вывод
@_bot.message_handler(commands="search")
def search_word_command(message):
    if len(message.text) < 9:
        _bot.reply_to(message, "Для поиска необходимых материалов,\nвведите команду '/search [запрос]")
        return

    uid = message.from_user.id
    settings = Settings.Settings.get_settings(uid)
    bf = BestFinder.BestFinder(settings[0], settings[1])
    top = bf.find_best(message.text[8:])
    msg = ""
    if len(top) == 0:
        _bot.reply_to(message, "Ничего не найдено")
        return

    for item in top:
        result = item.result
        msg += "{}:\nЦена: {} за {}\nДоступно в {}\nРейтинг: {}\n{}\n\n".format(result.full_name, result.price, result.per, result.available_at, result.rating, result.url)

    _bot.reply_to(message, msg)


# TODO - сделать нормальный вывод
# TODO - возможно добавить кнопку "добавить в избранное"
@_bot.message_handler(commands="history")
def history_command(message):
    uid = message.from_user.id
    msg = ""

    if Users.Users.is_admin(uid) and len(message.text) > 8:
        id = message.text[9:]
        msg += "История пользователя " + id + "\n\n"
    else:
        id = uid
        msg += "Ваша история:\n\n"

    history = Requests.Requests.get_user_requests_history(id)
    if len(history) == 0:
        _bot.reply_to(message, "История не найдена")
        return

    for request in history:
        msg += request.key + "\n" + request.value.full_name + "\n" + request.value.url + "\n\n"

    _bot.reply_to(message, msg)


# TODO - сделать нормальный вывод
# TODO - возможно добавить кнопку "убрать из избранного"
@_bot.message_handler(commands="favourites")
def favourites_command(message):
    uid = message.from_user.id
    msg = ""

    if Users.Users.is_admin(uid) and len(message.text) > 8:
        id = message.text[9:]
        msg += "Избранное пользователя " + id + "\n\n"
    else:
        id = uid
        msg += "Ваше избранное:\n\n"

    favourites = Favourites.Favourites.get_user_favourites(id)
    if len(favourites) == 0:
        _bot.reply_to(message, "Избранное не найдено")
        return

    for request in favourites:
        msg += request.key + "\n" + request.value.full_name + "\n" + request.value.url + "\n\n"

    _bot.reply_to(message, msg)


# TODO - сделать нормальный вывод
@_bot.message_handler(commands="pricehistory")
def price_history_command(message):
    # TODO - добавить выбор категории (ключевого слова) по кнопкам и вывод графика
    pass


@_bot.message_handler(commands="users")
def admin_users_command(message):
    uid = message.from_user.id

    if not Users.Users.is_admin(uid):
        return

    users = Users.Users.get_all_users()

    msg = "Список пользователей:\n\n"
    for user in users:
        msg += "id: {}\nРоль: {}\nДата начала: {}\n\n".format(user[0], user[1], user[2])

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
