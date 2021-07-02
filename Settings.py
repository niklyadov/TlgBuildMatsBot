import sqlite3


class Settings:

    @staticmethod
    def change_settings(user_id, top_count, ordering):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute(
                "update settings set top_count = ?, ordering_id = ? where user_id = ?",
                (top_count, ordering, user_id))
            dbc.commit()

    @staticmethod
    def get_settings(user_id):
        with sqlite3.connect("main.db") as dbc:
            cursor = dbc.cursor()
            return cursor.execute(
                "select top_count, ordering_id from settings where user_id = ?",
                (user_id,)).fetchall()[0]
