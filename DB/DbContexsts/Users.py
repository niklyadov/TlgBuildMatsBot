import sqlite3
from Models import StatisticModel
import Utils.DatesHandler as dh


class Users:

    # проверка на наличие пользователя в базе
    @staticmethod
    def is_registered(id):
        with sqlite3.connect("DB/main.db") as dbc:
            cr = dbc.cursor()
            cr.execute(
                "SELECT count(*) FROM Users WHERE telegram_id = ?",
                (id,))
            return not cr.fetchone()[0] == 0

    # проверка на супер-юзера
    @staticmethod
    def is_super_user(id):
        with sqlite3.connect("DB/main.db") as dbc:
            cr = dbc.cursor()
            cr.execute(
                "SELECT count(*) FROM Users WHERE telegram_id = ? and role_id = 1",
                (id,))
            return not cr.fetchone()[0] == 0

    # проверка на админа
    @staticmethod
    def is_admin(id):
        with sqlite3.connect("DB/main.db") as dbc:
            cr = dbc.cursor()
            cr.execute(
                "SELECT count(*) FROM Users WHERE telegram_id = ? and role_id <= 2",
                (id,))
            return not cr.fetchone()[0] == 0

    # добавим права админа юзеру
    @staticmethod
    def set_user_role(super_user_id, user_id, role):
        if Users.is_super_user(super_user_id):
            if role == 1:
                Users.transfer_super_user_rights(super_user_id, user_id)
            else:
                with sqlite3.connect("DB/main.db") as dbc:
                    dbc.execute(
                        "UPDATE Users SET role_id = ? where telegram_id = ?",
                        (role, user_id))
                    dbc.commit()

    # передача прав супер-юзера
    @staticmethod
    def transfer_super_user_rights(super_user_id, user_id):
        if Users.is_super_user(super_user_id):
            with sqlite3.connect("DB/main.db") as dbc:
                dbc.execute(
                    "UPDATE Users SET role_id = 1 where telegram_id = ?",
                    (user_id,))
                dbc.execute(
                    "UPDATE Users SET role_id = 2 where telegram_id = ?",
                    (super_user_id,))
                dbc.commit()

    # добавление пользователя в базу
    @staticmethod
    def register_user(id):
        with sqlite3.connect("DB/main.db") as dbc:
            dbc.execute(
                "INSERT INTO Users (telegram_id, role_id) VALUES(?, 3);",
                (id,))
            dbc.commit()

    # возвращает список всех зарегестрированных пользователей
    @staticmethod
    def get_all_users():
        with sqlite3.connect("DB/main.db") as dbc:
            cr = dbc.cursor()
            return cr.execute(
                "select telegram_id, (select name from roles where id = role_id), start_date from users").fetchall()

    # возвращает статистику по количеству зарегистрированных пользователей по дням
    @staticmethod
    def get_users_statistics_history(days_count):
        with sqlite3.connect("DB/main.db") as dbc:
            cursor = dbc.cursor()
            db_result = cursor.execute(
                "select date(round(julianday(start_date))) dt, count() "
                "from users where julianday() - julianday(start_date) < ? "
                "group by dt "
                "order by dt",
                (days_count, )).fetchall()

            days = dh.get_all_dates_from_now(days_count)
            return dh.fill_data(days, db_result)

