from json import JSONDecoder as decoder
from json import JSONEncoder as encoder


class JSON_Converter:

    @staticmethod
    def serialize(object):
        return encoder.encode(object)

    @staticmethod
    def deserialize(json_string):
        return decoder.decode(json_string)