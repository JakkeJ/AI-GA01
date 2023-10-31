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
            content = replace_contractions(content)

            for abbreviation in abbreviations:
                content = content.replace(abbreviation, abbreviation.replace('.', '__PERIOD__'))

            content = re.sub(r'[^\w\s\n—-]+´`', ' ', content)
            content = re.sub(r'[\d,”“]', '', content)
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
                
def replace_contractions(text):
    contractions = {
        "they've": "they have",
        "they're": "they are",
        "it's": "it is",
        "aren't": "are not",
        "can't": "cannot",
        "couldn't": "could not",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'll": "he will",
        "he's": "he is",
        "i'd": "I would",
        "i'll": "I will",
        "i'm": "I am",
        "let's": "let us",
        "she'd": "she would",
        "she'll": "she will",
        "she's": "she is",
        "that's": "that is",
        "there's": "there is",
        "they'd": "they would",
        "they'll": "they will",
        "we'd": "we would",
        "we're": "we are",
        "we've": "we have",
        "wasn't": "was not",
        "weren't": "were not",
        "what's": "what is",
        "where's": "where is",
        "who's": "who is",
        "won't": "will not",
        "wouldn't": "would not",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are",
        "must'nt": "must not"
    }

    contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))

    def replace(match):
        return contractions[match.group(0)]

    return contractions_re.sub(replace, text)