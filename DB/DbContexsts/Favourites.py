import sqlite3

from Utils.JSON_Converter import JSON_Converter


class Favourites:

    # добавление реквеста в избранное
    @staticmethod
    def add_request_to_favourites(user_id, full_name):
        with sqlite3.connect("DB/main.db") as dbc:
            dbc.execute(
                "insert into favourites (log_id) values ((select id from logs where user_id = ? and result like '%'||?||'%'))",
                (user_id, full_name.strip()))
            dbc.commit()

    # удаление реквеста из избранного
    @staticmethod
    def remove_request_from_favourites(user_id, full_name):
        with sqlite3.connect("DB/main.db") as dbc:
            dbc.execute(
                "delete from favourites where log_id = (select id from logs where user_id = ? and result like '%'||?||'%')",
                (user_id, full_name.strip()))
            dbc.commit()

    # возвращает список избранного данного пользователя
    @staticmethod
    def get_user_favourites(user_id):
        with sqlite3.connect("DB/main.db") as dbc:
            cursor = dbc.cursor()
            json_result = cursor.execute(
                "select date, result from logs where id in (select log_id from favourites where user_id = ?)",
                (user_id,)).fetchall()
            result = {}
            for date, item in json_result:
                if date not in result.keys():
                    result[date] = [JSON_Converter.deserialize(item)]
                else:
                    result[date].append(JSON_Converter.deserialize(item))
            return result
