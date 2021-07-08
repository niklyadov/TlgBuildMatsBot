from DB.DbContexsts import Requests, Key_Words
import threading


class HistoryAppender:
    def __init__(self, parsers):
        self.parsers = parsers

    def append(self, parser, key_words):
        with Requests.Requests.get_connection() as dbc:
            for key_word in key_words:
                result = parser.search(key_word)
                for request in result:
                    Requests.Requests.add_request(dbc, request)

    def append_history(self):
        threads = []
        for parser in self.parsers:
            thread = threading.Thread(target=self.append, args=(parser, Key_Words.key_words))
            threads.append(thread)
            thread.start()
        for th in threads:
            th.join()

