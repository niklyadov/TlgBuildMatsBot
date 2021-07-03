import sqlite3
import Key_Words
import StatisticModel
from JSON_Converter import JSON_Converter


class Requests:

    @staticmethod
    def add_request(user_id, request):
        with sqlite3.connect("main.db") as dbc:
            json_result = JSON_Converter.serialize(request.result)
            dbc.execute(
                "insert into requests (user_id, full_name, key_word_id, result) values (?, ?, (select id from key_words where word = ?), ?)",
                        (user_id, request.result.full_name, request.key_word, json_result))
            dbc.commit()

    @staticmethod
    def get_user_requests_history(user_id):
        with sqlite3.connect("main.db") as dbc:
            dbc.row_factory = lambda cursor, row: row[0]
            cursor = dbc.cursor()
            json_result = cursor.execute(
                "select date, result from requests where user_id = ?",
                                  (user_id,)).fetchall()
            result = {}
            for item in json_result:
                result[item[0]] = JSON_Converter.deserialize(item[1])
            return result

    @staticmethod
    def get_last_day_requests_by_key_word(key_word):
        with sqlite3.connect("main.db") as dbc:
            dbc.row_factory = lambda cursor, row: row[0]
            cursor = dbc.cursor()
            return cursor.execute(
                "select result from requests where key_word_id = (select id from key_words where word = ?) and julianday() - julianday(date) < 1",
                (key_word, )).fetchall()

    @staticmethod
    def get_last_day_requests_by_search_word(search_word):
        with sqlite3.connect("main.db") as dbc:
            dbc.row_factory = lambda cursor, row: row[0]
            cursor = dbc.cursor()
            return cursor.execute(
                "select result from requests where full_name like '%?%' and julianday() - julianday(date) < 1",
                (search_word,)).fetchall()

    @staticmethod
    def get_requests_statistics_history():
        statistics = {}
        with sqlite3.connect("main.db") as dbc:
            cursor = dbc.cursor()
            for word in Key_Words.key_words:
                db_result = cursor.execute(
                    "select date, result from requests").fetchall()
                stat = []
                for line in db_result:
                    price = JSON_Converter.deserialize(line[1]).price
                    stat.append(StatisticModel.StatisticModel(line[0], price))
                statistics[word] = stat
        return statistics
