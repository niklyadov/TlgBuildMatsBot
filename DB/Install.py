import sqlite3
import os.path


def install_db_if_not_exists():
    if not os.path.exists('DB/dist.sql'):
        print('dist.sql не найден')
        return
    if not os.path.exists('DB/main.db'):
        # создание базы данных
        print('Создание базы данных...')
        with sqlite3.connect('DB/main.db') as _connection:
            sql = open('DB/dist.sql', 'r', encoding='utf-8').read()
            _connection.executescript(sql)
            _connection.commit()
        print('База данных создана')