import sqlite3


class Settings:

    @staticmethod
    def change_settings(user_id, top_count, ordering):
        with sqlite3.connect("main.db") as dbc:
            dbc.execute("update settings set top_count = ?, ordering = ? where user_id = ?", (top_count, ordering, user_id))
            dbc.commit()

