from Document import Document

class Corpus:
    def __init__(self, name = ""):
        self._name = name
        self._corpus_list = []

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def corpus_list(self) -> list:
        return self._corpus_list
    
    @corpus_list.setter
    def corpus_list(self, corpus_list: list):
        self._corpus_list = corpus_list

    def append_corpus_item(self, document: Document):
        self._corpus_list.append(document)

    def delete_corpus_item(self, index):
        print(len(self._corpus_list))
        self._corpus_list.pop(index)
        print(len(self._corpus_list))

    def save_to_file(self, file_name):
        with open(file_name, "w") as file:
            for document in self._corpus_list:
                document.store_sentences_as_file(file)