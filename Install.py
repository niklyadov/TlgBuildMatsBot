import sqlite3

with sqlite3.connect('main.db') as _connection:
    sql = open('dist.sql', 'r').read()
    _connection.executescript(sql)
    _connection.commit()