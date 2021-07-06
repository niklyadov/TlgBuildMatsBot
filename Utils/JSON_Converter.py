import json


class JSON_Converter:

    # возвращает json-сериализованную версию объекта
    @staticmethod
    def serialize(obj):
        return json.dumps(obj, cls=MyEncoder, ensure_ascii=False)

    # возвращает python-десериализованную версию json-строки
    @staticmethod
    def deserialize(json_string):
        return json.loads(json_string)


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
