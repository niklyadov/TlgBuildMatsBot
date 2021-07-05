

class RequestModel:

    # key_word - ключевое слово, по которому был найден данный товар
    # result - объект класса ResultModel, хранящий информацию о полученном товаре
    # url - ссылка на страницу с товаром
    # full_name - полное название товара
    # price - цена товара в рублях
    # per - количество товара за его цену (шт, кг...)
    # rating - рейтинг товара
    # available_at - список магазинов/складов, в которых присутствует данный товар
    def __init__(self, key_word, url, full_name, price, per, rating, available_at):
        self.key_word = key_word
        self.url = url
        self.full_name = full_name
        self.price = price
        self.per = per
        self.rating = rating
        self.available_at = available_at


