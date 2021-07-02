import Requests
import JSON_Converter
import ResultModel

class BestFinder:

    def __init__(self, top_count, ordering):
        self.top_count = top_count
        self.ordering = ordering

    def find_best(self, search_word):
       # db_items = JSON_Converter.JSON_Converter.deserialize(Requests.Requests.get_last_day_requests())
        db_items = [ResultModel.ResultModel("url", "кирпич", 12.4, "шт", 5, ["ЧЛБ", "ЕКБ"]), ResultModel.ResultModel("url2", "камень", 13.4, "шт", 5, ["ЧЛБ2", "ЕКБ2"])]
        db_items = [i for i in db_items if search_word in i.name]

        if self.ordering == 1:
            sorted(db_items, key=lambda key: key.price)
        elif self.ordering == 2:
            sorted(db_items, key=lambda key: key.rating)
        elif self.ordering == 3:
            sorted(db_items, key=lambda key: key.name)
        else:
            sorted(db_items, key=lambda key: key.name, reverse=True)

        return db_items[:self.top_count]
