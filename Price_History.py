import sqlite3

from StatisticModel import StatisticModel


class Settings:

    @staticmethod
    def add_statistic(category, price):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute("insert into price_history (category_id, price) values (?, ?)", (category, price))
            dbc.commit()

    @staticmethod
    def get_statistics(category):
        with sqlite3.connect("main.db") as dbc:
            cursor = dbc.cursor()
            values = cursor.execute("select date, price from price_history where category_id = ?", (category,)).fetchall()
            statistics = []
            for pair in values:
                statistics.append(StatisticModel(pair[0], pair[1]))
            return statistics
