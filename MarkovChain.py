import random
from WordState import WordState

class MarkovChain:
    def __init__(self, corpus):
        self.corpus = corpus
        self.markov_chain = {}
        self.generated_sentences = []

    def build_markov_chain(self):
        sentences = []
        self.markov_chain = {}
        
        for doc in self.corpus.corpus_list:
            for sentence in doc.sentence_objects:
                sentences.append(sentence.sentence)

        for sentence in sentences:
            words = sentence.split()
            prev_word = "#"

            for word in words:
                if prev_word not in self.markov_chain:
                    self.markov_chain[prev_word] = WordState()

                self.markov_chain[prev_word].add_next_word(word)
                prev_word = word

        for current_word, word_state in self.markov_chain.items():
            total_transitions = sum(word_state._next_words.values())
            self.markov_chain[current_word]._next_words = {word: count / total_transitions for word, count in word_state._next_words.items()}

    def generate_text(self, seed=None, length=50):
        current_token = seed if seed is not None and seed != "#" else random.choice([key for key in self.markov_chain.keys() if key != "#"])
        text = [current_token]

        for _ in range(length):
            try:
                next_word_state = self.markov_chain.get(current_token)
                if next_word_state is None:
                    break

                next_token = next_word_state.get_next()
                if next_token is None:
                    break

                text.append(next_token)
                current_token = next_token
            except KeyError:
                print(f"Key '{current_token}' not found in Markov chain. Stopping text generation.")
                break

        self.generated_sentences.append(' '.join(text))