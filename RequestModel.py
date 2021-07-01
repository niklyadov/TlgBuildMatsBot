

class RequestModel:

    # request - запрос, который ввел пользователь
    # result - объект класса ResultModel, полученный путем парса сайта
    def __init__(self, request, result):
        self.request = request
        self.result = result
