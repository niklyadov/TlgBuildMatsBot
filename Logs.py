import sqlite3
import StatisticModel
import JSON_Converter


class Logs:

    # добавляет лог в базу
    @staticmethod
    def log(search_word, request, message, user_id):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute(
                "insert into logs(search_word, request_id, message_id, user_id) values (?, ?,(select id from messages where message = ?), ?);",
                (search_word, request, message, user_id))
            dbc.commit()

    # возвращает статистику количества запросов пользователей по дням
    @staticmethod
    def get_requests_statistics_history():
        with sqlite3.connect("main.db") as dbc:
            cursor = dbc.cursor()
            db_result = cursor.execute(
                "select round(julianday(date)), count() from logs group by round(julianday(date))").fetchall()
            stat = []
            for line in db_result:
                stat.append(StatisticModel.StatisticModel(line[0], line[1]))
        return stat

    # возвращает список реквестов пользователя
    @staticmethod
    def get_user_requests_history(user_id):
        with sqlite3.connect("main.db") as dbc:
            cursor = dbc.cursor()
            json_result = cursor.execute(
                "select date, (select result from requests where id = request_id) from logs where user_id = ?",
                                  (user_id,)).fetchall()
            result = {}
            for item in json_result:
                if item[1] is not None:
                    result[item[0]] = JSON_Converter.JSON_Converter.deserialize(item[1])
            return result
