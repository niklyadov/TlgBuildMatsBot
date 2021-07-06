import sqlite3
from Models import StatisticModel
from Utils import JSON_Converter


class Logs:

    # добавляет лог в базу
    @staticmethod
    def log(search_word, result, price, message, user_id):
        with sqlite3.connect("DB/main.db") as dbc:
            dbc.execute(
                "insert into logs(search_word, result, price, message_id, user_id) values (?, ?, ?, (select id from messages where message = ?), ?);",
                (search_word, result, price, message, user_id))
            dbc.commit()

    # возвращает статистику количества запросов пользователей по дням
    @staticmethod
    def get_requests_statistics_history(days_count):
        with sqlite3.connect("DB/main.db") as dbc:
            cursor = dbc.cursor()
            db_result = cursor.execute(
                "select round(julianday(date)), count() from logs where julianday() - julianday(date) < ? group by round(julianday(date))",
                (days_count, )).fetchall()
            stat = []
            for line in db_result:
                stat.append(StatisticModel.StatisticModel(line[0], line[1]))
        return stat

    # возвращает список реквестов пользователя
    @staticmethod
    def get_user_requests_history(user_id):
        with sqlite3.connect("DB/main.db") as dbc:
            cursor = dbc.cursor()
            json_result = cursor.execute(
                "select date, result from logs where user_id = ? order by date desc",
                                  (user_id,)).fetchall()

            result = {}
            for date, item in json_result:
                if date not in result.keys():
                    result[date] = [JSON_Converter.JSON_Converter.deserialize(item)]
                else:
                    result[date].append(JSON_Converter.JSON_Converter.deserialize(item))
            return result

