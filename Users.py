import sqlite3


class Users:

    # проверка на наличие пользователя в базе
    def is_registered(self, id):
        with sqlite3.connect("main.db") as dbc:
            cr = dbc.cursor()
            cr.execute(
                "SELECT count(*) FROM Users WHERE telegram_id = ?",
                (id,))
            return not cr.fetchone()[0] == 0

    # проверка на супер-юзера
    def is_super_user(self, id):
        with sqlite3.connect("main.db") as dbc:
            cr = dbc.cursor()
            cr.execute(
                "SELECT count(*) FROM Users WHERE telegram_id = ? and role_id = 1",
                (id,))
            return not cr.fetchone()[0] == 0

    # проверка на админа
    def is_admin(self, id):
        with sqlite3.connect("main.db") as dbc:
            cr = dbc.cursor()
            cr.execute(
                "SELECT count(*) FROM Users WHERE telegram_id = ? and role_id <= 2",
                (id,))
            return not cr.fetchone()[0] == 0

    # добавим права админа юзеру
    def set_user_role(self, super_user_id, user_id, role):
        if Users.is_super_user(super_user_id):
            if role == 1:
                Users.transfer_super_user_rights(super_user_id, user_id)
            else:
                with sqlite3.connect("main.db") as dbc:
                    dbc.execute(
                        "UPDATE Users SET role_id = ? where telegram_id = ?",
                        (role, user_id))
                    dbc.commit()

    # передача прав супер-юзера
    def transfer_super_user_rights(self, super_user_id, user_id):
        if Users.is_super_user(super_user_id):
            with sqlite3.connect("main.db") as dbc:
                dbc.execute(
                    "UPDATE Users SET role_id = 1 where telegram_id = ?",
                    (user_id,))
                dbc.execute(
                    "UPDATE Users SET role_id = 2 where telegram_id = ?",
                    (super_user_id,))
                dbc.commit()

    # добавление пользователя в базу
    def register_user(self, id):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute(
                "INSERT INTO Users (telegram_id, role_id) VALUES(?, 3);",
                (id,))
            dbc.commit()

    @staticmethod
    def get_all_users():
        with sqlite3.connect("main.db") as dbc:
            cr = dbc.cursor()
            return cr.execute(
                "select user_id, (select name from roles where id = role_id), start_date from users").fetchall()
