import re
from Sentence import Sentence

class Document:
    def __init__(self, name, file_path):
        self.name = name
        self.all_terms = {}
        self.word_count = 0
        self.sentences = []
        self.sentence_objects = []
        self.file_path = file_path

        with open(file_path) as file:
            content = file.read()

            abbreviations = ["Mr.", "Mrs.", "Miss.", "Dr.", "e.g.", "i.e.", "etc."]
            content = content.replace('\n', ' ')

            for abbreviation in abbreviations:
                content = content.replace(abbreviation, abbreviation.replace('.', '__PERIOD__'))

            content = re.sub(r'[^\w\s\n.?!-]+', ' ', content)
            self.sentences = re.split(r'[.!?]', content)
            for abbreviation in abbreviations:
                self.sentences = [sentence.replace(abbreviation.replace('.', '__PERIOD__'), abbreviation) for sentence in self.sentences]
            for sentence in self.sentences:
                self.sentence_objects.append(Sentence(sentence, source=self.name))
        self.sentences = []

    def store_sentences_as_file(self, file_name):
        with open(file_name, "a") as file:
            for i in self.sentence_objects:
                file.write(f'{i.sentence}\n')