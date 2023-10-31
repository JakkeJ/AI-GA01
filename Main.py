from Document import Document
from Corpus import Corpus
from MarkovChain import MarkovChain
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter import filedialog
import os
import subprocess
import platform

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Markov Chain Text Generator")
        self.resizable(False, False)
        self.minsize(800, 800)
        self.corpus = Corpus("My Corpus")
        self.corpus.append_corpus_item(Document("Your Mom Jokes", "yourmom.txt"))
        self.markov_chain = MarkovChain(self.corpus)
        self.markov_chain.build_markov_chain()
        self.sentence_count = 1

        self.style = Style(theme = "darkly")

        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill = 'x', side = tk.TOP)
        self.middle_frame = ttk.Frame(self)
        self.middle_frame.pack(fill = 'both', expand = True)
        self.bottom_frame = ttk.Frame(self, width = 800)
        self.bottom_frame.pack(fill = tk.X, side = tk.BOTTOM)
        self.bottom_frame.rowconfigure(9, weight = 1)
        self.bottom_frame.columnconfigure(9, weight = 1)

        self.sentence_length = 50

        self.seed_word = "your"
        self.main_window()


    def main_window(self):
        for frame in [self.top_frame, self.middle_frame, self.bottom_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
        label = ttk.Label(self.top_frame, text = "Markov Chain Text Generator")
        label.pack(padx = 5, pady = 5, side = tk.LEFT)
        settings_button = ttk.Button(self.top_frame, text = "Settings", command = self.open_settings, width = 8)
        settings_button.pack(padx = 5, pady = 5, side = tk.RIGHT)
        sentencebox_label = ttk.Label(self.middle_frame, text = "Generated sentences")
        sentencebox_label.pack(padx = 5, pady = 5, side = tk.TOP)
        self.sentence_box = tk.scrolledtext.ScrolledText(self.middle_frame, wrap = tk.WORD)
        self.sentence_box.pack(fill = 'both', expand = True, padx = 5, pady = 5)
        for i in range(10):
            self.bottom_frame.columnconfigure(i, weight = 1)

        self.sentence_count_label = ttk.Label(self.bottom_frame, text = "Number of sentences to generate")
        self.sentence_count_label.grid(row = 8, column = 0, padx = 5, pady = 5, sticky = 'w')

        self.sentence_count_entry = ttk.Spinbox(self.bottom_frame, from_ = 1, to = 10, width = 20, validate = "key", justify = 'center', validatecommand = (self.register(self._validate), "%P"))
        self.sentence_count_entry.grid(row = 9, column = 0, padx = 5, pady = 5, sticky = 'w')
        self.sentence_count_entry.insert(0, self.sentence_count)

        self.generate_button = ttk.Button(self.bottom_frame, text = "Generate sentences", command = self.generate_and_insert_text)
        self.generate_button.grid(row = 7, column = 9, padx = 5, pady = 5, sticky = 'e')
        self.generate_button.config(width = 20)

        self.save_file_name_label = ttk.Label(self.bottom_frame, text = "Generated sentences file name")
        self.save_file_name_label.grid(row = 8, column = 8, padx = 5, pady = 5, sticky = 'se')
        self.save_file_name_entry = ttk.Entry(self.bottom_frame, width = 20)
        self.save_file_name_entry.grid(row = 9, column = 8, padx = 5, pady = 5, sticky = 'e')

        self.save_button = ttk.Button(self.bottom_frame, text = "Save to file", width = 20, bootstyle = "success", command = self.save_generated_text)
        self.save_button.grid(row = 9, column = 9, padx = 5, pady = 5, sticky = 'ne')

        self.delete_button = ttk.Button(self.bottom_frame, width = 20, text = "Delete generated sentences", bootstyle = "danger", command = self.delete_generated_text)
        self.delete_button.grid(row = 8, column = 9, padx = 5, pady = 5, sticky = 'ne')
        self.update()

    def open_settings(self):
        for frame in [self.top_frame, self.middle_frame, self.bottom_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
        settings_label = ttk.Label(self.top_frame, text = "Markov Chain Text Generator - Settings")
        settings_label.pack(padx = 5, pady = 5, side = tk.LEFT)

        back_button = ttk.Button(self.top_frame, text = "Back", bootstyle = "primary", command = self.back_and_update, width = 8)
        back_button.pack(padx = 5, pady = 5, side = tk.RIGHT)

        self.corpus_listbox_label = ttk.Label(self.middle_frame, text = "Corpus files")
        self.corpus_listbox_label.pack(padx = 5, pady = 5, side = tk.TOP)
        self.corpus_listbox = tk.Listbox(self.middle_frame, selectmode = tk.SINGLE, height = 20)
        self.corpus_listbox.pack(fill = 'both', padx = 5, pady = 5)
        self.corpus_listbox.config(height = 25)
        for item in self.corpus.corpus_list:
            self.corpus_listbox.insert(tk.END, item.file_path)

        open_file_button = ttk.Button(self.bottom_frame, text = "Add files to Corpus", bootstyle = "primary", command = self.open_file_dialog)
        open_file_button.grid(row = 0, column = 0, padx = 5, pady = 5)

        save_corpus_name_label = ttk.Label(self.bottom_frame, text = "Processed sentences file name")
        save_corpus_name_label.grid(row = 0, column = 9)

        self.save_corpus_name_entry = ttk.Entry(self.bottom_frame)
        self.save_corpus_name_entry.grid(column = 9, row = 1)
        
        save_corpus_button = ttk.Button(self.bottom_frame, text = "Save corpus sentences to file", bootstyle = "success", command = self.save_corpus_to_file)
        save_corpus_button.grid(row = 2, column = 9, padx = 5, pady = 5)

        delete_button = ttk.Button(self.bottom_frame, text = "Delete Selected File from Corpus", bootstyle = "danger", command = self.delete_selected_item)
        delete_button.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.seed_word_label = ttk.Label(self.bottom_frame, text = "Seed word - default is 'your'")
        self.seed_word_label.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.seed_word_entry = ttk.Entry(self.bottom_frame)
        self.seed_word_entry.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.seed_word_entry.insert(0, self.seed_word)

        self.sentence_length_label = ttk.Label(self.bottom_frame, text = "Sentence length - default is 50")
        self.sentence_length_label.grid(row = 2, column = 1, padx = 5, pady = 5)

        self.sentence_length_entry = ttk.Spinbox(self.bottom_frame, from_ = 1, to = 100, validate = 'key', validatecommand = (self.register(self._validate), "%P"))
        self.sentence_length_entry.grid(row = 3, column = 1, padx = 5, pady = 5)
        self.sentence_length_entry.insert(0, self.sentence_length)
        
    def _validate(self, P):
        return P.isdigit()
    
    def delete_generated_text(self):
        self.markov_chain.generated_sentences = []
        self.sentence_box.delete("1.0", tk.END)
    
    def save_generated_text(self):
        file_name = self.save_file_name_entry.get()
        with open(file_name, "w") as f:
            for i in self.markov_chain.generated_sentences:
                f.write(f'{i}\n')
        dir_path = os.path.dirname(os.path.realpath(file_name))
        if platform.system()  ==  "Windows":
            os.startfile(dir_path)
        elif platform.system()  ==  "Darwin":
            subprocess.Popen(["open", dir_path])
        else:
            subprocess.Popen(["xdg-open", dir_path])

    def generate_and_insert_text(self):
        if len(self.corpus.corpus_list) > 0 and self.sentence_length > 1:
            self.sentence_count = self.sentence_count_entry.get()
            self.sentence_box.delete('1.0', tk.END)
            if self.seed_word  ==  "":
                self.seed_word = "#"
            for i in range(0, int(self.sentence_count)):
                self.markov_chain.generate_text(self.seed_word, self.sentence_length)
            for i in self.markov_chain.generated_sentences:
                self.sentence_box.insert(tk.END, f"• {i}\n")

    def open_file_dialog(self):
        filenames = filedialog.askopenfilenames(initialdir = os.getcwd(), title = "Select files", filetypes = (("text files", "*.txt"), ("csv files", "*.csv")))
        if filenames:
            for filename in filenames:
                self.corpus.append_corpus_item(Document("", filename))
            self.corpus_listbox.delete(0, tk.END)
            for item in self.corpus.corpus_list:
                self.corpus_listbox.insert(tk.END, item.file_path)

    def back_and_update(self):
        self.seed_word = self.seed_word_entry.get()
        self.sentence_length = int(self.sentence_length_entry.get())
        self.markov_chain.build_markov_chain()
        self.main_window()
        self.sentence_box.delete('1.0', tk.END)
        for i in self.markov_chain.generated_sentences:
            self.sentence_box.insert(tk.END, f"• {i}\n")

    def delete_selected_item(self):
        selected_item_index = self.corpus_listbox.curselection()
        if selected_item_index:
            self.corpus.delete_corpus_item(selected_item_index[0])
            self.corpus_listbox.delete(selected_item_index)
            
    def save_corpus_to_file(self):
        file_name = self.save_corpus_name_entry.get()
        self.corpus.save_to_file(file_name)
        dir_path = os.path.dirname(os.path.realpath(file_name))
        if platform.system()  ==  "Windows":
            os.startfile(dir_path)
        elif platform.system()  ==  "Darwin":
            subprocess.Popen(["open", dir_path])
        else:
            subprocess.Popen(["xdg-open", dir_path])
if __name__  ==  "__main__":
    app = GUI()
    app.mainloop()