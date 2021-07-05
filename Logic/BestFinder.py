from Models import RequestModel
from DB.DbContexsts import Logs
from Utils.JSON_Converter import JSON_Converter as json
from DB.DbContexsts.Requests import Requests


class BestFinder:

    def __init__(self, top_count, ordering, user_id):
        self.top_count = top_count
        self.ordering = ordering
        self.user_id = user_id

    # возвращает список RequestModel, отсортированный по ordering и ограниченный top_count
    def find_best(self, search_word):
        db_items = Requests.get_last_day_requests_by_search_word(search_word)

        db_items = [(i[0], json.deserialize(i[1])) for i in db_items]
        if self.ordering == 1:
            sorted(db_items, key=lambda key: key[1]['price'])
        elif self.ordering == 2:
            sorted(db_items, key=lambda key: key[1]['rating'])
        elif self.ordering == 3:
            sorted(db_items, key=lambda key: key[1]['full_name'])
        else:
            sorted(db_items, key=lambda key: key[1]['full_name'], reverse=True)

        result = db_items[:self.top_count]
        if len(result) >= self.top_count:
            log_message = 'successful'
        elif len(result) == 0:
            log_message = 'error'
        else:
            log_message = 'partially_done'

        # TODO - логирование по id
        Logs.Logs.log(search_word, json.serialize([i[1] for i in db_items]), log_message, self.user_id)

        return result
