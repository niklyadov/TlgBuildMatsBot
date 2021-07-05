import sqlite3

# создание базы данных
with sqlite3.connect('main.db') as _connection:
    sql = open('dist.sql', 'r', encoding='utf-8').read()
    _connection.executescript(sql)
    _connection.commit()