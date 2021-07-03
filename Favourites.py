import sqlite3

from JSON_Converter import JSON_Converter


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
            json_result = cursor.execute(
                "select date, result from requests where id = (select request_id from favourites where user_id = ?)",
                (user_id,)).fetchall()
            result = {}
            for item in json_result:
                result[item[0]] = JSON_Converter.deserialize(item[1])
            return result
