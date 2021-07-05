import telebot
from Logic import BestFinder, HistoryAppender, Parsers
import schedule
import threading
import time

from DB.DbContexsts import Users, Settings, Requests, RenewedFavourites, Logs, Key_Words, Favourites

_bot = telebot.TeleBot('1898682710:AAGGjRKCbh3a2zPzylGSqQ_Se9x3xSCPBBM')
_users = Users.Users()


# команда начала работы с ботом
@_bot.message_handler(commands=['start'])
def start_command(message):
    uid = message.from_user.id

    if not _users.is_registered(uid):
        _users.register_user(uid)
        _bot.reply_to(message, "Вы были зарегистрированы!")

    _bot.reply_to(message, "Для поиска необходимых материалов,\nвведите команду '/search [запрос]")


# команда, позволяющая искать товары
# TODO - сделать нормальный вывод
@_bot.message_handler(commands="search")
def search_word_command(message):
    if len(message.text) < 9:
        _bot.reply_to(message, "Для поиска необходимых материалов,\nвведите команду '/search [запрос]")
        return

    uid = message.from_user.id
    settings = Settings.Settings.get_settings(uid)
    bf = BestFinder.BestFinder(settings[0], settings[1], uid)
    top = bf.find_best(message.text[8:])
    msg = ""
    if len(top) == 0:
        _bot.reply_to(message, "Ничего не найдено")
        return

    for item in top:
        msg += "{}:\nЦена: {} за {}\nДоступно в {}\nРейтинг: {}\n{}\n\n".format(item.full_name, item.price, item.per, item.available_at, item.rating, item.url)

    _bot.reply_to(message, msg)


# команда, позволяющая посмотреть историю поисков
# (для обычного пользователя - только свою, для админа - любого пользователя)
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

    history = Logs.Logs.get_user_requests_history(id)
    if len(history) == 0:
        _bot.reply_to(message, "История не найдена")
        return

    _bot.reply_to(message, msg)
    for date, request in history.items():

        _bot.reply_to(message, 'Запрос от ' + date + ':')
        counter = 1

        for line in request:
            msg = prepare_msg(line, counter)
            counter += 1

            markup = telebot.types.InlineKeyboardMarkup()
            btn = telebot.types.InlineKeyboardButton(text="Добавить в избранное", reply_markup=markup,
                                                             callback_data="add_to_favourites")
            markup.add(btn)
            _bot.send_message(message.chat.id, msg, reply_markup = markup)


# команда, позволяющая посмотреть список избранного
# (для обычного пользователя - только свой, для админа - любого пользователя)
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

    _bot.reply_to(message, msg)
    for date, request in favourites.items():

        _bot.reply_to(message, 'Запрос от ' + date + ':')
        counter = 1

        for line in request:
            msg = prepare_msg(line, counter)
            counter += 1

            markup = telebot.types.InlineKeyboardMarkup()
            btn = telebot.types.InlineKeyboardButton(text="Убрать из избранного", reply_markup=markup,
                                                     callback_data="remove_from_favourites")
            markup.add(btn)
            _bot.send_message(message.chat.id, msg, reply_markup=markup)


days_count = 0


# команда, позволяющая посмотреть как изменялась цена на определенную категорию по дням
@_bot.message_handler(commands="pricehistory")
def price_history_command(message):
    days_count = message.text[len('/pricehistory '):]
    if not days_count.isnumeric() or len(message.text) <= len('/pricehistory '):
        _bot.reply_to(message, 'Для получения статистики по ценам используйте команду\n/pricehistory *промежуток времени до сегоднящнего дня в днях*')
        return

    key_words = Key_Words.key_words
    markup = telebot.types.InlineKeyboardMarkup()
    for word in key_words:
        markup.add(telebot.types.InlineKeyboardButton(text=word,
                                              callback_data="{}_category".format(word)))
    _bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=markup)


# команда, позволяющая узнать, какая роль у пользователя
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


# команда, позволяющая админу увидеть весь список пользоваетелей
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


# команда, позволяющая админу увидеть график количества зарегистрированных пользователей по дням
@_bot.message_handler(commands="usershistory")
def admin_users_history_command(message):
    uid = message.from_user.id
    if not Users.Users.is_admin(uid):
        return

    # TODO - сделать вывод графика зарегистрированных пользователей по дням
    # days_count = message.text[len('/usershistory '):]
    # Users.Users.get_users_statistics_history(days_count)
    pass


# команда, позволяющая админу увидеть график количества запросов пользователей по дням
@_bot.message_handler(commands="requestshistory")
def admin_requests_history_command(message):
    uid = message.from_user.id
    if not Users.Users.is_admin(uid):
        return

    # TODO - сделать вывод графика запросов от пользователей по дням
    # days_count = message.text[len('/requestshistory '):]
    # Logs.Logs.get_requests_statistics_history(days_count)
    pass


# команда, позволяющая супер-юзеру установить другому пользователю роль админа
# TODO !требуется тестирование!
@_bot.message_handler(commands=['setadmin'])
def super_user_set_admin_command(message):
    uid = message.from_user.id

    if not _users.is_registered(uid) or not _users.is_admin(uid):
        return

    if not _users.is_super_user(uid):
        _bot.reply_to(message, "❕ Вы должны быть суперпользователем")
        return

    if len(message.text) <= len('/setadmin '):
        _bot.reply_to(message, "❕ Синтаксис команды: \n/setadmin [id юзера]")
        return

    target_uid = message.text[len('/setadmin '):]

    if not target_uid.isnumeric():
        _bot.reply_to(message, "❌ Неправильный user id.")
        return

    target_uid = int(target_uid)

    if not _users.is_registered(target_uid):
        _bot.reply_to(message, "❌ Этот пользователь не зарегистрирован.")
        return

    if _users.is_admin(target_uid):
        _bot.reply_to(message, "❌ Этот пользователь уже является администратором.")
        return

    _users.set_user_role(uid, int(target_uid), 2)
    _bot.reply_to(message, "✅ пользователь " + str(target_uid) + " теперь является администратором.")


# команда, позволяющая супер-юзеру установить другому пользователю роль обычного пользователя
@_bot.message_handler(commands=['unsetadmin'])
def super_user_unset_admin_command(message):
    uid = message.from_user.id

    if not _users.is_registered(uid) or not _users.is_admin(uid):
        return

    if not _users.is_super_user(uid):
        _bot.reply_to(message, "❕ Вы должны быть суперпользователем")
        return

    if len(message.text) <= len('/unsetadmin '):
        _bot.reply_to(message, "❕ Синтаксис команды: \n/unsetadmin [id юзера]")
        return

    target_uid = message.text[len('/unsetadmin '):]

    if not target_uid.isnumeric():
        _bot.reply_to(message, "❌ Неправильный user id.")
        return

    target_uid = int(target_uid)

    if not _users.is_registered(target_uid):
        _bot.reply_to(message, "❌ Этот пользователь не зарегистрирован.")
        return

    if not _users.is_admin(target_uid):
        _bot.reply_to(message, "❌ Этот пользователь не является администратором.")
        return

    _users.set_user_role(uid, int(target_uid), 3)
    _bot.reply_to(message, "✅ пользователь " + str(target_uid) + " теперь не является администратором.")


# команда, позволяющая супер-юзеру передать права супер-юзера другому пользователю
# TODO !требуется тестирование!
@_bot.message_handler(commands=['superusertransfer'])
def super_user_transfer_command(message):
    uid = message.from_user.id

    if not _users.is_registered(uid) or not _users.is_admin(uid):
        return

    if not _users.is_super_user(uid):
        _bot.reply_to(message, "❕ Вы должны быть суперпользователем")
        return

    if len(message.text) <= len('/superusertransfer '):
        _bot.reply_to(message, "❕ Синтаксис команды: \n/superusertransfer [ваш id] [id юзера]")
        return

    [user_uid, target_uid] = message.text[len('/superusertransfer '):].split()

    if not target_uid.isnumeric() or not target_uid.isnumeric():
        _bot.reply_to(message, "❌ Вы должны ввести свой user id для подтверждения ({}).".format(uid))
        return

    target_uid = int(target_uid)
    user_uid = int(user_uid)

    if not user_uid == uid:
        _bot.reply_to(message, "❌ Подтверждающий id пользователя не верный.\n"
                               "Вы должны ввести свой user id для подтверждения ({}).".format(uid))
        return

    if not _users.is_registered(target_uid):
        _bot.reply_to(message, "❌ Этот пользователь не зарегистрирован.")
        return

    if _users.is_super_user(target_uid):
        _bot.reply_to(message, "❌ Этот пользователь уже является суперпользователем.")
        return

    _users.transfer_super_user_rights(uid, int(target_uid))
    _bot.reply_to(message, "✅ пользователь " + str(target_uid) + "теперь является суперпользователем.")


@_bot.message_handler(commands=['test'])
def test_command(message):
    pass


@_bot.callback_query_handler(func=lambda c: 'favourites' in c.data)
def favourites_buttons_handler(c):
    uid = c.from_user.id
    json = c.message.json['text']
    full_name = json.split('\n')[0][3:]
    if c.data == 'add_to_favourites':
        Favourites.Favourites.add_request_to_favourites(uid, full_name)
    if c.data == 'remove_from_favourites':
        Favourites.Favourites.remove_request_from_favourites(uid, full_name)


@_bot.callback_query_handler(func=lambda c: 'category' in c.data)
def favourites_buttons_handler(c):
    category = c.data.split('_')[0]
    show_history(c, category, Requests.Requests.get_price_statistics_history(category, days_count))


def show_history(c, category, data):
    msg = data  # TODO - обработать вывод данных по графику
    _bot.send_message(c.from_user.id, msg)
    pass


def prepare_msg(line, counter):
    msg = ""
    msg += '#{} '.format(counter)
    msg += ' {}\n'.format(line.full_name)
    msg += 'Цена: {}'.format(line.price)
    if line.per is not None:
        msg += ' за {}'.format(line.per)
    msg += '\n'
    if line.rating is None:
        line.rating = 'отсутствует'
    msg += 'Рейтинг: {}\n'.format(line.rating)
    msg += 'Доступно в:\n'
    for available_at in line.available_at:
        msg += ' -- {}\n'.format(available_at)
    msg += line.url
    msg += '\n\n'
    return msg


def cron_requests_update():
    history_appender = HistoryAppender.HistoryAppender(Parsers.parsers)
    history_appender.append_history()

    db_result = RenewedFavourites.RenewedFavourites.get_renewed_favourites()
    for user_id, full_name in db_result:
        _bot.send_message(user_id, "Изменилась цена на товар из вашего избранного под названием\n{}".format(full_name))

    RenewedFavourites.RenewedFavourites.clear_renewed_favourites()


def timer():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every().day.at("21:55").do(cron_requests_update)
threading.Thread(target=timer).start()

_bot.polling()