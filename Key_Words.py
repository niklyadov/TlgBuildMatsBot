import sqlite3


def get_key_words():
    with sqlite3.connect("main.db") as dbc:
        dbc.row_factory = lambda cursor, row: row[0]
        cursor = dbc.cursor()
        return cursor.execute(
            "select word from key_words").fetchall()


def get_key_word(string):
    for word in string:
        if word in key_words:
            return word


key_words = get_key_words()
