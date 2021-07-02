import sqlite3


def get_categories():
    with sqlite3.connect("main.db") as dbc:
        dbc.row_factory = lambda cursor, row: row[0]
        cursor = dbc.cursor()
        return cursor.execute("select name from categories").fetchall()


categories = get_categories()
