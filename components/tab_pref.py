import tkinter as tk
from tkinter import ttk
import Pmw
import os


class Preferences:
    def __init__(self, ui):
        # Main
        self.ui = ui
        self.frame_main = None
        self.frame_lang = None

        # Labels
        self.label_lang = None

        # Buttons
        self.btn_lang_en = None
        self.btn_lang_es = None
        self.btn_lang_fr = None
        self.btn_open_style_sett = None
        self.btn_future = None
        self.tip_lang_en = None
        self.tip_lang_es = None
        self.tip_lang_fr = None

        Pmw.initialise(self.ui.root)

    def create_tab(self) -> None:
        """Creates de PREFERENCES tab"""

        # Frame preferences
        self.frame_main = ttk.Frame(
            self.ui.notebook,
            style="Pref.TFrame"
        )
        self.frame_main.rowconfigure(0, weight=25)
        self.frame_main.rowconfigure(1, weight=10)
        self.frame_main.rowconfigure(2, weight=65)
        self.frame_main.columnconfigure(0, weight=100)

        self.frame_main.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["tab_pref"][0],
            pady=self.ui.grid_param["padding"]["tab_pref"][1]
        )
        self.ui.notebook.add(
            self.frame_main
        )

        # Frame preferences language
        self.frame_lang = ttk.Frame(
            self.frame_main,
            style="Lang.Pref.TFrame"
        )
        self.frame_lang.rowconfigure(0, weight=30)
        self.frame_lang.rowconfigure(1, weight=70)
        self.frame_lang.columnconfigure(0, weight=33)
        self.frame_lang.columnconfigure(1, weight=33)
        self.frame_lang.columnconfigure(2, weight=33)
        self.frame_lang.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["frame_pref_lang"][0],
            pady=self.ui.grid_param["padding"]["frame_pref_lang"][1]
        )
        # Label language
        self.label_lang = ttk.Label(
            self.frame_lang,
            style="Lang.Pref.TLabel",
            anchor="center"
        )
        self.label_lang.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["label_pref_lang"][0],
            pady=self.ui.grid_param["padding"]["label_pref_lang"][1]
        )

        ## Buttons language
        self.btn_lang_en = ttk.Button(
            self.frame_lang,
            command=self.action_swap_lang_en,
            style="Lang.TButton",
            takefocus=False
        )
        self.btn_lang_en.grid(
            row=1,
            column=0,
            padx=self.ui.grid_param["padding"]["btn_pref_lang_en"][0],
            pady=self.ui.grid_param["padding"]["btn_pref_lang_en"][1]
        )
        self.btn_lang_es = ttk.Button(
            self.frame_lang,
            command=self.action_swap_lang_es,
            style="Lang.TButton",
            takefocus=False
        )
        self.btn_lang_es.grid(
            row=1,
            column=1,
            padx=self.ui.grid_param["padding"]["btn_pref_lang_es"][0],
            pady=self.ui.grid_param["padding"]["btn_pref_lang_es"][1]
        )
        self.btn_lang_fr = ttk.Button(
            self.frame_lang,
            command=self.action_swap_lang_fr,
            style="Lang.TButton",
            takefocus=False
        )
        self.btn_lang_fr.grid(
            row=1,
            column=2,
            padx=self.ui.grid_param["padding"]["btn_pref_lang_fr"][0],
            pady=self.ui.grid_param["padding"]["btn_pref_lang_fr"][1]
        )

        ## Button open user settings
        self.btn_open_style_sett = ttk.Button(
            self.frame_main,
            command=self.action_open_style_sett_file,
            style="OpenStyleSett.TButton",
            takefocus=False
        )
        self.btn_open_style_sett.grid(
            row=1,
            column=0,
            padx=self.ui.grid_param["padding"]["btn_pref_open_style_sett"][0],
            pady=self.ui.grid_param["padding"]["btn_pref_open_style_sett"][1]
        )

        ## Button Future
        self.btn_future = ttk.Button(
            self.frame_main,
            command=lambda: print(":)"),
            style="Future.TButton",
            takefocus=False
        )
        self.btn_future.grid(
            row=2,
            column=0,
            padx=self.ui.grid_param["padding"]["btn_pref_future"][0],
            pady=self.ui.grid_param["padding"]["btn_pref_future"][1]
        )

        self.update_tab()

    def update_tab(self) -> None:
        """Updates the PREFERENCES tab and its components"""

        self.ui.notebook.tab(self.frame_main, text=self.ui.disp_txt["pref"])
        self.label_lang.configure(text=self.ui.disp_txt["label"]["lang"])
        self.btn_lang_en.configure(image=self.ui.img["en_flag"])
        self.btn_lang_es.configure(image=self.ui.img["es_flag"])
        self.btn_lang_fr.configure(image=self.ui.img["fr_flag"])
        self.btn_open_style_sett.configure(
            text=self.ui.disp_txt["btn"]["open_style_sett"]
        )
        self.btn_future.configure(
            text=self.ui.disp_txt["btn"]["future"],
            image=self.ui.img["wip"],
            compound=tk.TOP
        )

        # Tooltips
        self.tip_lang_en = Pmw.Balloon(self.ui.root)
        self.tip_lang_en.bind(self.btn_lang_en, self.ui.disp_txt["btn"]["lang_en"])
        self.tip_lang_es = Pmw.Balloon(self.ui.root)
        self.tip_lang_es.bind(self.btn_lang_es, self.ui.disp_txt["btn"]["lang_es"])
        self.tip_lang_fr = Pmw.Balloon(self.ui.root)
        self.tip_lang_fr.bind(self.btn_lang_fr, self.ui.disp_txt["btn"]["lang_fr"])

    def action_open_style_sett_file(self) -> None:
        """Opens the style settings file"""

        if not self.ui.pu.popup:
            os.system("notepad.exe " + self.ui.uset.user_settings["style"])

    def action_swap_lang_en(self) -> None:
        """Swaps and updates the language to english"""

        if not self.ui.pu.popup:
            self.ui.update_lang("en")
        self.ui.update_tabs()

    def action_swap_lang_es(self) -> None:
        """Swaps and updates the language to spanish"""

        if not self.ui.pu.popup:
            self.ui.update_lang("es")
        self.ui.update_tabs()

    def action_swap_lang_fr(self) -> None:
        """Swaps and updates the language to french"""

        if not self.ui.pu.popup:
            self.ui.update_lang("fr")
        self.ui.update_tabs()
