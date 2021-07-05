import sqlite3


class RenewedFavourites:

    # полностью очищает таблицу Renewed_Favourites
    @staticmethod
    def clear_renewed_favourites():
        with sqlite3.connect("main.db") as dbc:
            dbc.execute(
                "delete from renewed_favourites")
            dbc.commit()

    # возвращает список избранного пользователей, на которых изменилась цена
    @staticmethod
    def get_renewed_favourites():
        with sqlite3.connect("main.db") as dbc:
            cursor = dbc.cursor()
            db_result = cursor.execute(
                "select favourite_id from renewed_favourites").fetchall()
            return db_result