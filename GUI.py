"""
Module for the Compiler GUI
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

class CompWindow:
    def __init__(self, message):
        self._components = {
            'root': tk.Tk()
        }
        self.init_window(message)

    def init_window(self, message):
        print(message)
        self.root.title("Compilador")
        self._components['text_edit'] = ScrolledText(self.root, width=60, height=20)
        self._components['lex'] = tk.Button(self.root, text='Get tokens')
        self._components['parse'] = tk.Button(self.root, text='Parse Code')

        self._components['table'] = ttk.Treeview(self.root, columns=("Type",
                                                                     "Lexeme",
                                                                     "Description"),
                                                 show="headings",
                                                 height=5)
        self._components['table'].heading("Type", text="Type")
        self._components['table'].heading("Lexeme", text="Lexeme")
        self._components['table'].heading("Description", text="Description")

        self._components['text_edit'].pack()
        self._components['lex'].pack()
        self._components['parse'].pack()
        self._components['table'].pack()

    def start_window(self):
        self.root.mainloop()

    @property
    def root(self):
        return self._components['root']


