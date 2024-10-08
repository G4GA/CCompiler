"""
Module for the Compiler GUI
"""

import tkinter as tk
from tkinter import scrolledtext
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

    def start_window(self):
        self.root.mainloop()

    @property
    def root(self):
        return self._components['root']


