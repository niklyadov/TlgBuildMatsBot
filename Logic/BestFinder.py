from Models import RequestModel
from DB.DbContexsts import Logs
from Utils.JSON_Converter import JSON_Converter as json
from DB.DbContexsts.Requests import Requests
import Utils.Float_Conv as flt


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
            db_items = sorted(db_items, key=lambda key: flt.try_convert_to_float(
                key[1]['price'].strip().replace(",", ".").replace(" ", "")))
        elif self.ordering == 2:
            db_items = sorted(db_items, key=lambda key: flt.try_convert_to_float(key[1]['rating']))
        elif self.ordering == 3:
            db_items = sorted(db_items, key=lambda key: key[1]['full_name'])
        else:
            db_items = sorted(db_items, key=lambda key: key[1]['full_name'], reverse=True)

        result = db_items[:self.top_count]
        if len(result) >= self.top_count:
            log_message = 'successful'
        elif len(result) == 0:
            log_message = 'error'
        else:
            log_message = 'partially_done'

        for id, item in result:
            Logs.Logs.log(search_word, json.serialize(item), log_message, self.user_id)

        return result
