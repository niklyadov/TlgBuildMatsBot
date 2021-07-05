import Requests
import Key_Words
import threading


class HistoryAppender:
    def __init__(self, parsers):
        self.parsers = parsers

    def append(self, parser, key_word):
        Requests.Requests.add_request(parser.search(key_word))

    def append_history(self):
        for parser in self.parsers:
            for key_word in Key_Words.key_words:
                thread = threading.Thread(target=self.append, args=(parser, key_word))
                thread.start()


