

class ResultModel:
    
    # url - ссылка на страницу с товаром
    # name - полное название товара
    # price - цена товара в рублях
    # per - количество товара за его цену (шт, кг...)
    # rating - рейтинг товара
    # available_at - список магазинов/складов, в которых присутствует данный товар
    def __init__(self, url, name, price, per, rating, available_at):
        self.url = url
        self.name = name
        self.price = price
        self.per = per
        self.rating = rating
        self.available_at = available_at
