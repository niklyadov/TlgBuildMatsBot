import sqlite3


class Favourites:

    @staticmethod
    def add_request_to_favourites(user_id, full_name):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute(
                "insert into favourites (request_id) values ((select request_id from requests where user_id = ? and full_name = ?))",
                (user_id, full_name))
            dbc.commit()

    @staticmethod
    def remove_request_from_favourites(user_id, full_name):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute(
                "delete from favourites where request_id = (select request_id from requests where user_id = ? and full_name = ?)",
                (user_id, full_name))
            dbc.commit()

    @staticmethod
    def get_user_favourites(user_id):
        with sqlite3.connect("main.db") as dbc:
            dbc.row_factory = lambda cursor, row: row[0]
            cursor = dbc.cursor()
            return cursor.execute(
                "select result from requests where request_id = (select request_id from favourites where user_id = ?)",
                (user_id,)).fetchall()
