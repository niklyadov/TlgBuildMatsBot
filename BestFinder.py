import Requests
import JSON_Converter
import Key_Words
import RequestModel
import Logs

class BestFinder:

    def __init__(self, top_count, ordering, user_id):
        self.top_count = top_count
        self.ordering = ordering
        self.user_id = user_id

    # возвращает список RequestModel, отсортированный по ordering и ограниченный top_count
    def find_best(self, search_word):
       #db_items = JSON_Converter.JSON_Converter.deserialize(Requests.Requests.get_last_day_requests_by_search_word(search_word))
        db_items = [RequestModel.RequestModel("кирпич", RequestModel.ResultModel("http://www.stackoverflow.com", 'кирпич обыкновенный', 12.4, 'шт', 5, ['ЧЛБ', 'ЕКБ'])),
                    RequestModel.RequestModel("камень", RequestModel.ResultModel("http://www.stackoverflow.com", 'камень необыкновенный 10000', 1023.4, 'кг', 5, ['ЧЛБ', 'ЕКБ', 'МСК']))]

        if self.ordering == 1:
            sorted(db_items, key=lambda key: key.result.price)
        elif self.ordering == 2:
            sorted(db_items, key=lambda key: key.result.rating)
        elif self.ordering == 3:
            sorted(db_items, key=lambda key: key.result.full_name)
        else:
            sorted(db_items, key=lambda key: key.result.full_name, reverse=True)

        result = db_items[:self.top_count]
        if len(result) >= self.top_count:
            log_message = 'successful'
        elif len(result) == 0:
            log_message = 'error'
        else:
            log_message = 'partially_done'

        # TODO - логирование по id
        Logs.Logs.log(search_word, 1, log_message, self.user_id)

        return result
