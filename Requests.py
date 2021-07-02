import sqlite3
from JSON_Converter import JSON_Converter


class Requests:

    @staticmethod
    def add_request(user_id, request):
        with sqlite3.connect("main.db") as dbc:
            json_request = JSON_Converter.serialize(request)
            dbc.execute("insert into requests (user_id, result) values (?, ?)", (user_id, json_request))
            dbc.commit()

    @staticmethod
    def get_user_requests(user_id):
        with sqlite3.connect("main.db") as dbc:
            dbc.row_factory = lambda cursor, row: row[0]
            cursor = dbc.cursor()
            return cursor.execute("select result from requests where user_id = ?", (user_id,)).fetchall()

    @staticmethod
    def get_last_day_requests():
        with sqlite3.connect("main.db") as dbc:
            dbc.row_factory = lambda cursor, row: row[0]
            cursor = dbc.cursor()
            return cursor.execute("select result from requests where julianday() - julianday(date) < 1").fetchall()