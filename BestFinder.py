import Requests
import JSON_Converter
import Key_Words
import RequestModel

class BestFinder:

    def __init__(self, top_count, ordering):
        self.top_count = top_count
        self.ordering = ordering

    def find_best(self, search_word):
       #db_items = JSON_Converter.JSON_Converter.deserialize(Requests.Requests.get_last_day_requests_by_search_word(search_word))
        db_items = [RequestModel.RequestModel("url", "кирпич", 12.4, "шт", 5, ["ЧЛБ", "ЕКБ"]),
                    RequestModel.RequestModel("url2", "камень", 13.4, "шт", 5, ["ЧЛБ2", "ЕКБ2"])]

        if self.ordering == 1:
            sorted(db_items, key=lambda key: key.price)
        elif self.ordering == 2:
            sorted(db_items, key=lambda key: key.rating)
        elif self.ordering == 3:
            sorted(db_items, key=lambda key: key.name)
        else:
            sorted(db_items, key=lambda key: key.name, reverse=True)

        return db_items[:self.top_count]
