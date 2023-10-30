import random as rand

class WordState:
    def __init__(self):
        self._next_words = {}  # A dict with all the next words and their frequencies.

    def add_next_word(self, next_word):
        if next_word in self._next_words:
            self._next_words[next_word] += 1
        else:
            self._next_words[next_word] = 1

    def has_next(self):
        return bool(self._next_words)

    def get_next(self):
        if self.has_next():
            return rand.choices(list(self._next_words.keys()), weights=list(self._next_words.values()), k=1)[0]
        else:
            return None