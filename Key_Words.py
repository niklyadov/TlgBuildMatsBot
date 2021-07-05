import sqlite3


# возвращает список всех ключевых слов
def get_key_words():
    with sqlite3.connect("main.db") as dbc:
        dbc.row_factory = lambda cursor, row: row[0]
        cursor = dbc.cursor()
        return cursor.execute(
            "select word from key_words").fetchall()


# возвращает ключевое слово, содержащееся в данном сообщении
def get_key_word(string):
    for word in string:
        if word in key_words:
            return word


key_words = get_key_words()
