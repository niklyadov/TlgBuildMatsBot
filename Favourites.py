import sqlite3

from JSON_Converter import JSON_Converter


class Favourites:

    # добавление реквеста в избранное
    @staticmethod
    def add_request_to_favourites(user_id, full_name):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute(
                "insert into favourites (log_id) values ((select id from logs where user_id = ? and result like '%'||?||'%'))",
                (user_id, full_name))
            dbc.commit()

    # удаление реквеста из избранного
    @staticmethod
    def remove_request_from_favourites(user_id, full_name):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute(
                "delete from favourites where log_id = (select id from logs where user_id = ? and result like '%'||?||'%')",
                (user_id, full_name))
            dbc.commit()

    # возвращает список избранного данного пользователя
    @staticmethod
    def get_user_favourites(user_id):
        with sqlite3.connect("main.db") as dbc:
            dbc.row_factory = lambda cursor, row: row[0]
            cursor = dbc.cursor()
            json_result = cursor.execute(
                "select date, (select result from requests where id = request_id) from logs where id = (select log_id from favourites where user_id = ?)",
                (user_id,)).fetchall()
            result = {}
            for item in json_result:
                result[item[0]] = JSON_Converter.deserialize(item[1])
            return result
