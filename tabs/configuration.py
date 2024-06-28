import tkinter as tk
from tkinter import ttk


class Configuration:
    def __init__(self, ui):
        self.ui = ui

        self.frame_main = ttk.Frame(
            self.ui.notebook,
            style="Conf.TFrame"
        )
