import sqlite3

_connection = sqlite3.connect('main.db')
sql = open('dist.sql', 'r').read()
_connection.executescript(sql)
_connection.commit()