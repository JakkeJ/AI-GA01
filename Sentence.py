class Sentence:
    def __init__(self, sentence: str, source = ""):
        self._source = source
        self._sentence = sentence.lower().strip()

    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, source):
        self._source = source

    @property
    def sentence(self):
        return self._sentence
    
    @sentence.setter
    def sentence(self, sentence):
        self._sentence = sentence