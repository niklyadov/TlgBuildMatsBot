import sqlite3

class Users:

    # проверка на наличие пользователя в базе
    def isRegistered(self, id):
        with sqlite3.connect("main.db") as dbc:
            cr = dbc.cursor()
            cr.execute("SELECT count(*) FROM Users WHERE telegram_id = ?", (id,))
            return not cr.fetchone()[0] == 0

    # проверка на админа
    def isAdmin(self, id):
        with sqlite3.connect("main.db") as dbc:
            cr = dbc.cursor()
            cr.execute("SELECT count(*) FROM Users WHERE telegram_id = ? and role_id = 2", (id,))
            return not cr.fetchone()[0] == 0

    # добавим права админа юзеру
    def setAdmin(self, id):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute("UPDATE Users SET role_id = 2 where telegram_id = ?", (id,))
            dbc.commit()

    # добавление пользователя в базу
    def registerUser(self, id):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute("INSERT INTO Users (telegram_id, role_id) VALUES(?, 3);", (id,))
            dbc.commit()
