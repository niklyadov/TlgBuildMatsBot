import Requests
import Key_Words
import threading


class HistoryAppender:
    def __init__(self, parsers):
        self.parsers = parsers

    def append(self, parser, key_word):
        result = parser.search(key_word)
        for request in result:
            Requests.Requests.add_request(request)

    def append_history(self):
        threads = []
        for parser in self.parsers:
            for key_word in Key_Words.key_words:
                thread = threading.Thread(target=self.append, args=(parser, key_word))
                threads.append(thread)
                thread.start()
        for th in threads:
            th.join()


