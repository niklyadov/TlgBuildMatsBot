import telebot
from Logic import BestFinder, HistoryAppender, Parsers, Graphics
import schedule
import threading
import time
import os


from DB.DbContexsts import Users, Settings, Requests, RenewedFavourites, Logs, Key_Words, Favourites

_bot = telebot.TeleBot('1898682710:AAGGjRKCbh3a2zPzylGSqQ_Se9x3xSCPBBM')
_users = Users.Users()


# команда начала работы с ботом
@_bot.message_handler(commands=['help', 'start'])
def start_command(message):
    uid = message.from_user.id

    if not _users.is_registered(uid):
        _users.register_user(uid)
        _bot.reply_to(message, "Вы были зарегистрированы!")

    _bot.reply_to(message, "Для поиска необходимых материалов,\nвведите команду '/search [запрос]")


# команда, позволяющая искать товары
@_bot.message_handler(commands=["search"])
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
        _bot.reply_to(message, "Ничего не найдено \U0001F614")
        return

    _bot.reply_to(message, "По вашему запросы были найдены следующие товары:")
    counter = 1
    for id, value in top:
        msg = prepare_msg(value, counter)
        counter += 1

        _bot.send_message(message.from_user.id, msg)


_ordering = {1: 'цена', 2: 'рейтинг', 3: 'а-я', 4: 'я-а'}


# команда, позволяющая пользователю просматривать и зименять свои настройки
@_bot.message_handler(commands=["settings"])
def settings_command(message):
    uid = message.from_user.id
    settings = Settings.Settings.get_settings(uid)
    if len(message.text) < 11:
        _bot.reply_to(message, "Ваши настройки:"
                               "\nКоличество показываемых товаров: {}".format(settings[0]) +
                               "\nСортировка по: {}".format(_ordering[settings[1]]) +
                               settings_help())
        return
    set = message.text.split()
    if len(set) != 3:
        _bot.reply_to(message, settings_help())
        return
    top_count = int(set[1])
    ordering = set[2]
    if top_count <= 0 or top_count >= 9:
        _bot.reply_to(message, settings_help())
        return

    order = None
    for key, value in _ordering.items():
        if ordering == value:
            order = key
    if order is None:
        _bot.reply_to(message, settings_help())
        return

    Settings.Settings.change_settings(uid, top_count, order)
    _bot.reply_to(message, '✅ Настройки сохранены')


def settings_help():
    return "\nДля того, чтобы изменить настройки введите команду:" \
           "\n/settings [кол-во товаров (1-9)] [сортировать по (цена, рейтинг, а-я, я-а)]"


history = {}


# команда, позволяющая посмотреть историю поисков
# (для обычного пользователя - только свою, для админа - любого пользователя)
@_bot.message_handler(commands=["history"])
def history_command(message):
    uid = message.from_user.id
    msg = ""

    if Users.Users.is_admin(uid) and len(message.text) > 8:
        id = message.text[9:]
        msg += "История пользователя " + id + "\n\n"
    else:
        id = uid
        msg += "Ваша история:\n\n"

    global history
    history = Logs.Logs.get_user_requests_history(id)

    if len(history) == 0:
        _bot.reply_to(message, "История не найдена")
        return

    history_count = 5
    small_history = {}
    if len(history) >= history_count:
        for key, value in history.items():
            if len(small_history) < history_count:
                small_history[key] = value
    else:
        small_history = history
    _bot.reply_to(message, msg)

    show_user_history(message, small_history)

    if len(history) >= history_count:
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton(text="Посмотреть всю историю", reply_markup=markup,
                                                 callback_data="show_history")
        markup.add(btn)
        _bot.send_message(message.chat.id, 'История ранее:', reply_markup=markup)


def show_user_history(message, history):
    for date, requests in history.items():

        counter = 1
        for request in requests:
            msg = 'Запрос от 📅 ' + date + ':\n'
            msg += prepare_msg(request, counter)
            counter += 1

            markup = telebot.types.InlineKeyboardMarkup()
            btn = telebot.types.InlineKeyboardButton(text="⭐️Добавить в избранное ⭐️", reply_markup=markup,
                                                             callback_data="add_to_favourites")
            markup.add(btn)
            _bot.send_message(message.chat.id, msg, reply_markup = markup)


# команда, позволяющая посмотреть список избранного
# (для обычного пользователя - только свой, для админа - любого пользователя)
@_bot.message_handler(commands=["favourites"])
def favourites_command(message):
    uid = message.from_user.id
    msg = ""

    if Users.Users.is_admin(uid) and len(message.text) > len('/favourites '):
        id = message.text[len('/favourites '):]
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

        counter = 1

        for line in request:
            msg = 'Запрос от 📅 ' + date + ':\n'
            msg += prepare_msg(line, counter)
            counter += 1

            markup = telebot.types.InlineKeyboardMarkup()
            btn = telebot.types.InlineKeyboardButton(text="❌ Убрать из избранного ❌", reply_markup=markup,
                                                     callback_data="remove_from_favourites")
            markup.add(btn)
            _bot.send_message(message.chat.id, msg, reply_markup=markup)


days_count = 0


# команда, позволяющая посмотреть как изменялась цена на определенную категорию по дням
@_bot.message_handler(commands=["pricehistory"])
def price_history_command(message):
    global days_count
    days_count = message.text[len('/pricehistory '):]
    if not days_count.isnumeric() or len(message.text) <= len('/pricehistory '):
        _bot.reply_to(message, 'Для получения статистики по ценам используйте команду'
                               '\n/pricehistory [промежуток времени до сегоднящнего дня в днях]')
        return
    days_count = int(days_count)
    if days_count <= 1:
        _bot.reply_to(message, 'Количество дней должно быть больше одного')
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
            if _users.is_super_user(uid):
                _bot.reply_to(message, "Вы супер-юзер")
            else:
                _bot.reply_to(message, "Вы админ")
        else:
            _bot.reply_to(message, "Вы обычный пользователь")
    else:
        _bot.reply_to(message, "Вы не зарегистрированы. Как вы это сделали?")


# команда, позволяющая админу увидеть весь список пользоваетелей
@_bot.message_handler(commands=["users"])
def admin_users_command(message):
    uid = message.from_user.id

    if not Users.Users.is_admin(uid):
        return

    users = Users.Users.get_all_users()

    _bot.reply_to(message, "Список пользователей:\n\n")
    for user in users:
        _bot.send_message(message.from_user.id, "id: {}\nРоль: {}\nДата начала: {}\n\n".format(user[0], user[1], user[2]))


# команда, позволяющая админу увидеть график количества зарегистрированных пользователей по дням
@_bot.message_handler(commands=["usershistory"])
def admin_users_history_command(message):
    uid = message.from_user.id
    if not Users.Users.is_admin(uid):
        return

    days_count = get_days_from_command(message, "usershistory")
    if days_count is None:
        return

    stat = Users.Users.get_users_statistics_history(int(days_count))
    save_path = Graphics.Graphics.get_history_histogram(stat, 'Статистика количества зарегистрированных пользователей по дням')
    send_image(message.from_user.id, save_path)


# команда, позволяющая админу увидеть график количества запросов пользователей по дням
@_bot.message_handler(commands=["requestshistory"])
def admin_requests_history_command(message):
    uid = message.from_user.id
    if not Users.Users.is_admin(uid):
        return

    days_count = get_days_from_command(message, "requestshistory")
    if days_count is None:
        return

    stat = Logs.Logs.get_requests_statistics_history(int(days_count))
    save_path = Graphics.Graphics.get_history_histogram(stat, 'Статистика количества запросов пользователей по дням')
    send_image(message.from_user.id, save_path)


def get_days_from_command(message, command):
    if not len(message.text) > len('/{} '.format(command)):
        _bot.reply_to(message, 'Формат команды: /{} [промежуток времени до сегоднящнего дня в днях]'.format(command))
        return None

    days_count = message.text[len('/{} '.format(command)):]
    if not days_count.isnumeric():
        _bot.reply_to(message, 'Количество дней должно быть целым числом')
        return None
    return days_count


def send_image(uid, save_path):
    img = open(save_path, 'rb')
    _bot.send_photo(uid, photo=img)
    img.close()
    os.remove(save_path)


# команда, позволяющая супер-юзеру установить другому пользователю роль админа
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
@_bot.message_handler(commands=['superusertransfer'])
def super_user_transfer_command(message):
    uid = message.from_user.id

    if not _users.is_registered(uid) or not _users.is_admin(uid):
        return

    if not _users.is_super_user(uid):
        _bot.reply_to(message, "❕ Вы должны быть суперпользователем")
        return

    if len(message.text) <= len('/superusertransfer '):
        _bot.reply_to(message, "❕ Синтаксис команды: \n/superusertransfer [id юзера]")
        return

    [user_uid, target_uid] = message.text[len('/superusertransfer '):].split()

    if not user_uid.isnumeric() or not target_uid.isnumeric():
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


@_bot.callback_query_handler(func=lambda c: 'favourites' in c.data)
def favourites_buttons_handler(c):
    uid = c.from_user.id
    json = c.message.json['text']
    full_name = json.split('\n')[1][5:]
    if c.data == 'add_to_favourites':
        try:
            Favourites.Favourites.add_request_to_favourites(uid, full_name)
        except Exception as e:
            _bot.reply_to(c.message, "❌ Вы не можете добавить в избранное, то, что там уже есть")
    if c.data == 'remove_from_favourites':
        Favourites.Favourites.remove_request_from_favourites(uid, full_name)
        _bot.delete_message(c.from_user.id, c.message.message_id)
    _bot.answer_callback_query(c.id)


@_bot.callback_query_handler(func=lambda c: 'history' in c.data)
def history_buttons_handler(c):
    global history
    show_user_history(c.message, history)
    history = {}
    _bot.answer_callback_query(c.id)


@_bot.callback_query_handler(func=lambda c: 'category' in c.data)
def categories_buttons_handler(c):
    category = c.data.split('_')[0]
    show_history(c, category, Requests.Requests.get_price_statistics_history(category, days_count))
    _bot.answer_callback_query(c.id)


def show_history(c, category, stat):
    # TODO - Дарья: сделать вывод графика цен по дням по данной категории
    _bot.send_message(c.from_user.id, 'Статистика по категории - {}:'.format(category))
    save_path = Graphics.Graphics.get_history_plot(stat, 'Статистика изменения цены по категории {}'.format(category))
    send_image(c.from_user.id, save_path)


def prepare_msg(line, counter):
    msg = ""
    msg += '{}\ufe0f\u20e3 '.format(counter)
    msg += ' {}\n'.format(line['full_name'])
    msg += 'Цена: {}'.format(line['price'])
    if line['per'] is not None:
        msg += ' за {}'.format(line['per'])
    msg += '\n'
    if line['rating'] is not None and line['rating'] != 0:
        msg += 'Рейтинг: {}\n'.format(line['rating'])
    #msg += 'Доступно в:\n'
    #for available_at in line['available_at']:
       # msg += ' -- {}\n'.format(available_at)
    if line['url'] is not None:
        msg += '\n'
        msg += line['url']
    msg += '\n\n'
    return msg


def cron_requests_update():
    print('#: Начало обновления данных')
    history_appender = HistoryAppender.HistoryAppender(Parsers.parsers)
    history_appender.append_history()
    print('#: Конец обновления данных')

    db_result = RenewedFavourites.RenewedFavourites.get_renewed_favourites()
    for user_id, old_price, new_price, full_name in db_result:
        if old_price != new_price:
            if old_price > new_price:
                symbol = "⤵️"
            else:
                symbol = "⤴️"

            _bot.send_message(user_id, "Изменение цены на товар из вашего избранного:"
                                       "\n{}"
                                       "\nСтарая цена: {}"
                                       "\nНовая цена: {} - {}".format(full_name, old_price, new_price, symbol))

    RenewedFavourites.RenewedFavourites.clear_renewed_favourites()


def timer():
    while True:
        schedule.run_pending()
        time.sleep(60)


schedule.every().day.at("18:00").do(cron_requests_update)
threading.Thread(target=timer).start()

while True:
    try:
        _bot.polling(none_stop=True)

    except Exception as e:
        print('#: Бот перестал работать по причине:')
        print(e)
        print('\n')
        time.sleep(15)
