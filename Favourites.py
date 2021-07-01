import sqlite3


class Favourites:

    @staticmethod
    def add_last_request_to_favourites(user_id):
        with sqlite3.connect("main.db") as dbc:
            dbc.row_factory = lambda cursor, row: row[0]
            cursor = dbc.cursor()
            latest_id = cursor.execute("select id from requests where user_id = ? and date = (select max(strftime(%s, date)) from requests where user_id = ?)", (user_id,)).fetchall()
            dbc.execute("insert into favourites (request_id) values (?)", (latest_id,))
            dbc.commit()
