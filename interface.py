import os
import json
import Pmw
import logging as log
from tkinter import *
from tkinter import ttk
from user_settings import *


class Interface:
    def __init__(self, logic) -> None:
        # Main
        self.logic = logic
        self.uset = UserSettings()
        self.style = None

        # Components
        self.notebook = None
        ## RUN
        self.tab_run = None
        self.btn_run_roll = None
        self.btn_run_clear = None
        self.table_run = None
        ## CONF
        self.tab_conf = None
        self.frame_conf_act = None
        self.btn_conf_open_config_file = None
        self.btn_conf_add = None
        self.btn_conf_edit = None
        self.btn_conf_del = None
        self.table_conf = None
        self.tip_add = None
        self.tip_edit = None
        self.tip_del = None
        ## PREF
        self.tab_pref = None
        self.frame_pref_lang = None
        self.label_pref_lang = None
        self.btn_pref_lang_en = None
        self.btn_pref_lang_es = None
        self.btn_pref_lang_fr = None
        self.btn_pref_open_style_sett = None
        self.btn_pref_future = None
        self.tip_lang_en = None
        self.tip_lang_es = None
        self.tip_lang_fr = None

        # Displayed text (language settings)
        self.lang = None
        self.disp_txt = None
        self.update_lang()
        
        # Row selected
        self.table_conf_sel = None
        
        # Columns to display in each table
        self.table_run_cols = ("participant", "assigned")
        self.table_conf_cols = ("#0", "family_id", "participant", "age", "exceptions")

        # Windows
        self.root = Tk()
        self.fixed_win = {
            "minsize": (640, 480),
            "dim": (800, 600),
            "pos": (0, 0)
        }
        self.set_root()
        self.popup_edit = None

        # Data
        self.img = {
            "add": PhotoImage(file="./images/add.png"),
            "edit": PhotoImage(file="./images/edit.png"),
            "del": PhotoImage(file="./images/del.png"),
            "checked": PhotoImage(file="./images/checked.png"),
            "unchecked": PhotoImage(file="./images/unchecked.png"),
            "en_flag": PhotoImage(file="./images/en.png"),
            "es_flag": PhotoImage(file="./images/es.png"),
            "fr_flag": PhotoImage(file="./images/fr.png"),
            "wip": PhotoImage(file="./images/wip.png")
        }
        self.table_run_data = {}

        # Style
        self.grid_param = self.get_grid_param()
        self.style_static = self.get_style_static()
        self.style_dynamic = self.get_style_dynamic()

        # Columns & rows
        self.run_col_width = (self.fixed_win["dim"][0] - 2 * (self.style_static["settings"]["TNotebook"]["configure"]["padding"][0] + self.style_static["settings"]["TFrame"]["configure"]["padding"][0])) // len(self.table_run_cols) - 3
        self.conf_first_col_width = 16 * 2 + self.img["checked"].width()
        self.conf_col_width = (self.fixed_win["dim"][0] - 2 * (self.style_static["settings"]["TNotebook"]["configure"]["padding"][0]+ + self.style_static["settings"]["TFrame"]["configure"]["padding"][0]) - self.conf_first_col_width) // (len(self.table_conf_cols) - 1) - 3
        self.table_conf_last_index = 0
        
        # Initialization
        Pmw.initialise(self.root)
        self.set_style()
        self.update_style()
        self.set_tabs()

    def update_lang(self, lang: str = None) -> None:
        """Updates the language data on the interface module"""
        
        def load_lang(language) -> dict:
            """Retrieves the selected language data"""
            with open("./user_settings/lang.json", encoding="utf-8") as f:
                raw = f.read()
                return json.loads(raw)[language]
        if lang:
            self.uset.update_lang(lang)
            self.uset.load_user_settings()
        self.lang = self.uset.get_lang()
        self.disp_txt = load_lang(self.lang)

    def set_root(self) -> None:
        """Generates the root window with its dimensions and position"""
        
        self.root.title("Secret Santa")
        self.root.iconbitmap("secret_santa.ico")
        self.root.minsize(
            self.fixed_win["minsize"][0],
            self.fixed_win["minsize"][1]
        )

        # Calculate window position (relatively to its dimensions)
        self.fixed_win["pos"] = (
            self.root.winfo_screenwidth() // 2 - (self.fixed_win["dim"][0] // 2),
            self.root.winfo_screenheight() // 2 - (self.fixed_win["dim"][1] // 2),
        )

        # Apply dimensions and position to the window
        self.root.geometry(
            f'{self.fixed_win["dim"][0]}x{self.fixed_win["dim"][1]}+{self.fixed_win["pos"][0]}+{self.fixed_win["pos"][1]}'
        )
        
        # Grid configuration
        self.root.rowconfigure(0, weight=100)
        self.root.columnconfigure(0, weight=100)

    @staticmethod
    def get_grid_param() -> dict:
        """Retrieves the static style data"""
        
        with open("./user_settings/styles/static.json") as f:
            static = f.read()
            return json.loads(static)["grid"]

    @staticmethod
    def get_style_static() -> dict:
        """Retrieves the static style data"""
        
        with open("./user_settings/styles/static.json") as f:
            static = f.read()
            return json.loads(static)["style"]

    def get_style_dynamic(self) -> dict:
        """Retrieves the dynamic style data"""
        
        with open(self.uset.user_settings["style"]) as f:
            dynamic = f.read()
            return json.loads(dynamic)

    def set_style(self) -> None:
        """Attempts to create a new style and applies it to the interface"""
        
        # Style creation
        self.style = ttk.Style()
        try:
            self.style.theme_create(**self.style_static)
        except:
            log.info(f'Theme {self.style_static["themename"]} already exists')
        
        # Style application
        self.style.theme_use(self.style_static["themename"])

    def update_style(self) -> None:
        """Updates the static style data with the dynamic style data"""
        
        for component, modes in self.style_dynamic.items():
            for mode in modes:
                if mode == "configure":
                    self.style.configure(
                        component,
                        **modes[mode]
                    )
                elif mode == "map":
                    self.style.map(
                        component,
                        **modes[mode]
                    )
                else:
                    log.info(f'Ignoring style mode {mode}')

    def set_tabs(self) -> None:
        """Set the notebook and its tabs"""
        
        self.notebook = ttk.Notebook(self.root)
        self.create_tab_run()
        self.create_tab_conf()
        self.create_tab_pref()
        self.notebook.grid(
            row=0,
            column=0,
            sticky=NSEW
        )

    def create_tab_run(self) -> None:
        """Creates the RUN tab"""
        
        # TFrame
        self.tab_run = ttk.Frame(
            self.notebook,
            style="Run.TFrame"
        )
        self.tab_run.rowconfigure(0, weight=20)
        self.tab_run.rowconfigure(1, weight=80)
        self.tab_run.columnconfigure(0, weight=100)
        self.tab_run.grid(
            row=0,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["tab_run"][0],
            pady=self.grid_param["padding"]["tab_run"][1]
        )
        self.notebook.add(
            self.tab_run
        )

        # Actions frame
        self.frame_run_act = ttk.Frame(
            self.tab_run,
            style="Act.Run.TFrame"
        )
        self.frame_run_act.rowconfigure(0, weight=50)
        self.frame_run_act.rowconfigure(1, weight=50)
        self.frame_run_act.columnconfigure(0, weight=100)
        self.frame_run_act.grid(
            row=0,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["frame_run_act"][0],
            pady=self.grid_param["padding"]["frame_run_act"][1]
        )

        ## Buttons
        self.btn_run_roll = ttk.Button(
            self.frame_run_act,
            command=self.action_run,
            style="Roll.TButton",
            takefocus=False
        )
        self.btn_run_roll.grid(
            row=0,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_run_roll"][0],
            pady=self.grid_param["padding"]["btn_run_roll"][1]
        )
        self.btn_run_clear = ttk.Button(
            self.frame_run_act,
            command=self.action_clear,
            style="Clear.TButton",
            takefocus=False
        )
        self.btn_run_clear.grid(
            row=1,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_run_clear"][0],
            pady=self.grid_param["padding"]["btn_run_clear"][1]
        )

        # Treeview
        self.table_run = ttk.Treeview(
            self.tab_run,
            style="TableRun.Treeview"
        )
        self.table_run.configure(columns=self.table_run_cols)
        self.table_run.grid(
            row=1,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["table_run"][0],
            pady=self.grid_param["padding"]["table_run"][1]
        )
        
        ## Tags
        self.table_run.tag_configure(
            "oddrow",
            background="#C7DEB1"
        )
        self.update_tab_run()

    def update_tab_run(self) -> None:
        """Updates the RUN tab and its components"""
        
        self.notebook.tab(self.tab_run, text=self.disp_txt["run"])
        self.btn_run_roll.configure(text=self.disp_txt["btn"]["roll"])
        self.btn_run_clear.configure(text=self.disp_txt["btn"]["clear"])
        # self.table_run.configure(height=20)
        
        ## Headings & columns
        self.table_run.heading(
            "#0",
            text=""
        )
        self.table_run.column(
            "#0",
            stretch=NO,
            minwidth=0,
            width=0
        )
        for i, v in enumerate(self.table_run_cols):
            self.table_run.heading(
                v,
                text=self.disp_txt["tab_run_table_headings"][i],
                anchor=CENTER
            )
            self.table_run.column(
                v,
                stretch=YES,
                # minwidth=self.fixed_style["treeview.column"]["minwidth"],
                width=self.run_col_width,
                anchor=CENTER
            )
        
        self.empty_table(self.table_run)
        for i, (name, assigned) in enumerate(self.table_run_data.items()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            values = (f'{name.title()}', f'{", ".join([p.name for p in assigned])}')
            self.table_run.insert("", "end", values=values, tags=tag)

    def create_tab_conf(self) -> None:
        """Creates the CONFIGURATION tab"""
        
        # Frame
        self.tab_conf = ttk.Frame(
            self.notebook,
            style="Conf.TFrame"
        )
        self.tab_conf.rowconfigure(0, weight=20)
        self.tab_conf.rowconfigure(1, weight=80)
        self.tab_conf.columnconfigure(0, weight=100)
        self.tab_conf.grid(
            row=0,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["tab_conf"][0],
            pady=self.grid_param["padding"]["tab_conf"][1]
        )
        self.notebook.add(
            self.tab_conf
        )
        
        # Actions frame
        self.frame_conf_act = ttk.Frame(
            self.tab_conf,
            style="Act.Conf.TFrame"
        )
        self.frame_conf_act.rowconfigure(0, weight=50)
        self.frame_conf_act.rowconfigure(1, weight=50)
        self.frame_conf_act.columnconfigure(0, weight=33)
        self.frame_conf_act.columnconfigure(1, weight=33)
        self.frame_conf_act.columnconfigure(2, weight=33)
        self.frame_conf_act.grid(
            row=0,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["frame_conf_act"][0],
            pady=self.grid_param["padding"]["frame_conf_act"][1]
        )

        # Buttons
        self.btn_conf_open_config_file = ttk.Button(
            self.frame_conf_act,
            command=self.action_open_config_file,
            style="OpenConfigFile.TButton",
            takefocus=False
        )
        self.btn_conf_open_config_file.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_conf_open_config"][0],
            pady=self.grid_param["padding"]["btn_conf_open_config"][1]
        )
        self.btn_conf_add = ttk.Button(
            self.frame_conf_act,
            command=self.action_add_member,
            style="Add.TButton",
            takefocus=False
        )
        self.btn_conf_add.grid(
            row=1,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_conf_add"][0],
            pady=self.grid_param["padding"]["btn_conf_add"][1]
        )
        self.btn_conf_edit = ttk.Button(
            self.frame_conf_act,
            command=self.action_edit_member,
            style="Edit.TButton",
            takefocus=False
        )
        self.btn_conf_edit.grid(
            row=1,
            column=1,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_conf_edit"][0],
            pady=self.grid_param["padding"]["btn_conf_edit"][1]
        )
        self.btn_conf_del = ttk.Button(
            self.frame_conf_act,
            command=self.action_del_member,
            style="Del.TButton",
            takefocus=False
        )
        self.btn_conf_del.grid(
            row=1,
            column=2,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_conf_del"][0],
            pady=self.grid_param["padding"]["btn_conf_del"][1]
        )

        # Treeview
        self.table_conf = ttk.Treeview(
            self.tab_conf,
            style="TableConf.Treeview"
        )
        self.table_conf.configure(columns=self.table_conf_cols[1:])
        self.table_conf.grid(
            row=1,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["table_conf"][0],
            pady=self.grid_param["padding"]["table_conf"][1]
        )
        
        ## Tags
        self.table_conf.tag_configure(
            "oddrow",
            background="#C7DEB1"
        )
        self.table_conf.tag_configure(
            "selected",
            background="#478ADD"
        )

        self.update_tab_conf()

    def update_tab_conf(self) -> None:
        """Updates the CONFIGURATION tab and its components"""
        
        self.notebook.tab(self.tab_conf, text=self.disp_txt["conf"])
        self.btn_conf_open_config_file.configure(text=self.disp_txt["btn"]["open_config"])
        self.btn_conf_add.configure(image=self.img["add"])
        self.btn_conf_edit.configure(image=self.img["edit"])
        self.btn_conf_del.configure(image=self.img["del"])
        
        # Tooltips
        self.tip_add = Pmw.Balloon(self.root)
        self.tip_add.bind(self.btn_conf_add, self.disp_txt["btn"]["add_conf_table"])
        self.tip_edit = Pmw.Balloon(self.root)
        self.tip_edit.bind(self.btn_conf_edit, self.disp_txt["btn"]["edit_conf_table"])
        self.tip_del = Pmw.Balloon(self.root)
        self.tip_del.bind(self.btn_conf_del, self.disp_txt["btn"]["del_conf_table"])
        
        ## Headings & columns
        for i, v in enumerate(self.table_conf_cols):
            if i == 0:
                self.table_conf.heading(
                    v,
                    text=self.disp_txt["tab_conf_table_headings"][i],
                    anchor=CENTER
                )
                self.table_conf.column(
                    v,
                    stretch=NO,
                    minwidth=self.conf_first_col_width,
                    width=self.conf_first_col_width
                )
            else:
                self.table_conf.heading(
                    v,
                    text=self.disp_txt["tab_conf_table_headings"][i],
                    anchor=CENTER
                )
                self.table_conf.column(
                    v,
                    stretch=YES,
                    width=self.conf_col_width,
                    anchor=CENTER
                )
        
        self.empty_table(self.table_conf)
        self.logic.read_participants()
        self.logic.parse_participants()
        for i, member in enumerate(self.logic.participants.values()):
            if self.table_conf_sel == i:
                tags = "selected"
            else:
                tags = ("evenrow" if i % 2 == 0 else "oddrow")
            img = self.img["checked"] if member.enabled else self.img["unchecked"]
            values = (f'{member.family_id}',
                      f'{member.name.title()}',
                      f'{member.age.title()}',
                      f'{", ".join([e.title() for e in member.exceptions])}')
            if "enabled" in tags:
                self.table_conf.insert(
                    "",
                    "end",
                    id=self.table_conf_last_index,
                    image=img,
                    values=values,
                    tags=tags
                )
            else:
                self.table_conf.insert(
                    "", 
                    "end",
                    id=self.table_conf_last_index,
                    image=img,
                    values=values,
                    tags=tags
                )
            self.table_conf_last_index += 1

    def create_tab_pref(self) -> None:
        """Creates de PREFERENCES tab"""
        
        # Frame preferences
        self.tab_pref = ttk.Frame(
            self.notebook,
            style="Pref.TFrame"
        )
        self.tab_pref.rowconfigure(0, weight=25)
        self.tab_pref.rowconfigure(1, weight=10)
        self.tab_pref.rowconfigure(2, weight=65)
        self.tab_pref.columnconfigure(0, weight=100)

        self.tab_pref.grid(
            row=0,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["tab_pref"][0],
            pady=self.grid_param["padding"]["tab_pref"][1]
        )
        self.notebook.add(
            self.tab_pref
        )
        
        # Frame preferences language 
        self.frame_pref_lang = ttk.Frame(
            self.tab_pref,
            style="Lang.Pref.TFrame"
        )
        self.frame_pref_lang.rowconfigure(0, weight=30)
        self.frame_pref_lang.rowconfigure(1, weight=70)
        self.frame_pref_lang.columnconfigure(0, weight=33)
        self.frame_pref_lang.columnconfigure(1, weight=33)
        self.frame_pref_lang.columnconfigure(2, weight=33)
        self.frame_pref_lang.grid(
            row=0,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["frame_pref_lang"][0],
            pady=self.grid_param["padding"]["frame_pref_lang"][1]
        )
        # Label language
        self.label_pref_lang = ttk.Label(
            self.frame_pref_lang,
            style="Lang.Pref.TLabel",
        )
        self.label_pref_lang.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky=NSEW,
            padx=self.grid_param["padding"]["label_pref_lang"][0],
            pady=self.grid_param["padding"]["label_pref_lang"][1]
        )
        
        ## Buttons language
        self.btn_pref_lang_en = ttk.Button(
            self.frame_pref_lang,
            command=self.action_swap_lang_en,
            style="Lang.TButton",
            takefocus=False
        )
        self.btn_pref_lang_en.grid(
            row=1,
            column=0,
            padx=self.grid_param["padding"]["btn_pref_lang_en"][0],
            pady=self.grid_param["padding"]["btn_pref_lang_en"][1]
        )
        self.btn_pref_lang_es = ttk.Button(
            self.frame_pref_lang,
            command=self.action_swap_lang_es,
            style="Lang.TButton",
            takefocus=False
        )
        self.btn_pref_lang_es.grid(
            row=1,
            column=1,
            padx=self.grid_param["padding"]["btn_pref_lang_es"][0],
            pady=self.grid_param["padding"]["btn_pref_lang_es"][1]
        )
        self.btn_pref_lang_fr = ttk.Button(
            self.frame_pref_lang,
            command=self.action_swap_lang_fr,
            style="Lang.TButton",
            takefocus=False
        )
        self.btn_pref_lang_fr.grid(
            row=1,
            column=2,
            padx=self.grid_param["padding"]["btn_pref_lang_fr"][0],
            pady=self.grid_param["padding"]["btn_pref_lang_fr"][1]
        )
        
        ## Button open user settings
        self.btn_pref_open_style_sett = ttk.Button(
            self.tab_pref,
            command=self.action_open_style_sett_file,
            style="OpenStyleSett.TButton",
            takefocus=False
        )
        self.btn_pref_open_style_sett.grid(
            row=1,
            column=0,
            padx=self.grid_param["padding"]["btn_pref_open_style_sett"][0],
            pady=self.grid_param["padding"]["btn_pref_open_style_sett"][1]
        )
        
        ## Button Future
        self.btn_pref_future = ttk.Button(
            self.tab_pref,
            command=lambda: print(":)"),
            style="Future.TButton",
            takefocus=False
        )
        self.btn_pref_future.grid(
            row=2,
            column=0,
            padx=self.grid_param["padding"]["btn_pref_future"][0],
            pady=self.grid_param["padding"]["btn_pref_future"][1]
        )
        
        self.update_tab_pref()

    def update_tab_pref(self) -> None:
        """Updates the PREFERENCES tab and its components"""
        
        self.notebook.tab(self.tab_pref, text=self.disp_txt["pref"])
        self.label_pref_lang.configure(text=self.disp_txt["label"]["lang"])
        self.btn_pref_lang_en.configure(image=self.img["en_flag"])
        self.btn_pref_lang_es.configure(image=self.img["es_flag"])
        self.btn_pref_lang_fr.configure(image=self.img["fr_flag"])
        self.btn_pref_open_style_sett.configure(
            text=self.disp_txt["btn"]["open_style_sett"]
        )
        self.btn_pref_future.configure(
            text=self.disp_txt["btn"]["future"],
            image=self.img["wip"],
            compound=TOP
        )
        
        # Tooltips
        self.tip_lang_en = Pmw.Balloon(self.root)
        self.tip_lang_en.bind(self.btn_pref_lang_en, self.disp_txt["btn"]["lang_en"])
        self.tip_lang_es = Pmw.Balloon(self.root)
        self.tip_lang_es.bind(self.btn_pref_lang_es, self.disp_txt["btn"]["lang_es"])
        self.tip_lang_fr = Pmw.Balloon(self.root)
        self.tip_lang_fr.bind(self.btn_pref_lang_fr, self.disp_txt["btn"]["lang_fr"])

    def empty_table(self, table: ttk.Treeview) -> None:
        """Empties the config table and resets its index"""
        
        table.delete(*table.get_children())
        self.table_conf_last_index = 0

    def action_run(self) -> None:
        """Retrieves the randomized paired data"""
        
        self.table_run_data = self.logic.run()
        self.update_tab_run()

    def action_clear(self) -> None:
        """Clears the retrieved data and the treeview"""
        
        self.table_run_data.clear()
        self.update_tab_run()

    def action_open_config_file(self) -> None:
        """Opens the configuration file"""
        
        os.system("notepad.exe " + self.uset.user_settings["input_file"])

    def action_add_member(self) -> None:
        """Adds a new member to the config file"""
        
        print("Adding new member!")
        self.update_tab_conf()
    
    def action_edit_member(self) -> None:
        """Edits an existing member from the config file"""
        
        if self.table_conf_sel is not None:
            self.edit_member(list(self.logic.participants.values())[self.table_conf_sel])
            self.update_tab_conf()

    def action_del_member(self) -> None:
        """Deletes an existing member from the config file"""
        
        print("Deleting member!")
        self.update_tab_conf()

    def action_open_style_sett_file(self) -> None:
        """Opens the style settings file"""
        
        os.system("notepad.exe " + self.uset.user_settings["style"])

    def action_swap_check(self, row: int) -> None:
        """Swaps the member status (enabled, disabled)"""
        
        member = list(self.logic.participants.keys())[row]
        self.logic.participants[member].enabled = not self.logic.participants[member].enabled

    def action_swap_lang_en(self) -> None:
        """Swaps and updates the language to english"""
        
        self.update_lang("en")
        self.update_tab_run()
        self.update_tab_conf()
        self.update_tab_pref()
    
    def action_swap_lang_es(self) -> None:
        """Swaps and updates the language to spanish"""
        
        self.update_lang("es")
        self.update_tab_run()
        self.update_tab_conf()
        self.update_tab_pref()
    
    def action_swap_lang_fr(self) -> None:
        """Swaps and updates the language to french"""
        
        self.update_lang("fr")
        self.update_tab_run()
        self.update_tab_conf()
        self.update_tab_pref()

    def action_save_edit(self) -> None:
        """Saves changes made in the editing popup"""
        
        print("Saving!")

    def action_cancel_edit(self) -> None:
        """Cancels and closes the editing popup"""
        
        self.popup_edit.destroy()
        self.popup_edit.update()

    @staticmethod
    def disable_resizing(_) -> str:
        """Disables the column resizing"""
        
        return "break"

    def on_click_config(self, event: Event) -> str | None:
        """Called on click event"""
        
        region = self.table_conf.identify("region", event.x, event.y)
        if region == "separator":
            return self.disable_resizing(event)
        elif region == "tree" or region == "cell":
            try:
                row = int(self.table_conf.identify_row(event.y))
                col = int(self.table_conf.identify_column(event.x)[1:])
                if col == 0:
                    self.action_swap_check(row)
                    self.logic.update_config_file()
                    self.update_tab_conf()
                else:
                    self.table_conf_sel = row if self.table_conf_sel != row else None
                    print(self.table_conf_sel)
                    self.update_tab_conf()
            except:
                log.error("Cell coordinates cannot be calculated")

    def edit_member(self, member):
        """Opens a window where member data can be edited"""
        # TODO Pendiente de añadir languages a los botones (y labels?)
        
        member_attrs = vars(member)
        
        # Popup window
        try:
            self.popup_edit.destroy()
        except:
            pass
        self.popup_edit = Toplevel()
        self.popup_edit.rowconfigure(0, weight=90)
        self.popup_edit.rowconfigure(1, weight=10)
        self.popup_edit.columnconfigure(0, weight=100)
        
        ## Frames
        frame_data = Frame(self.popup_edit)
        [frame_data.rowconfigure(i, weight=100//len(member_attrs)) for i in range(len(member_attrs))]
        frame_data.columnconfigure(0, weight=100)
        frame_data.grid(
            row=0,
            column=0,
            sticky=NSEW
        )
        frame_actions = Frame(self.popup_edit)
        frame_actions.rowconfigure(0, weight=100)
        frame_actions.columnconfigure(0, weight=50)
        frame_actions.columnconfigure(1, weight=50)
        frame_actions.grid(
            row=1,
            column=0,
            sticky=NSEW
        )
        
        # Member data
        for attr_index, (attr_name, attr_value) in enumerate(member_attrs.items()):
            frame_attr = Frame(frame_data)
            frame_attr.columnconfigure(0, weight=20)
            frame_attr.columnconfigure(1, weight=80)
            if type(attr_value) == list:
                if len(attr_value) > 0:
                    for row_index in range(len(attr_value)):
                        frame_attr.rowconfigure(row_index, weight=100//len(attr_value))
                else:
                    frame_attr.rowconfigure(0, weight=100)
                frame_attr.grid(row=attr_index, column=0, sticky=NSEW)
                label_box = Label(frame_attr, height=1, text=f'{attr_name}: '.title())
                label_box.grid(row=0, column=0, sticky="NSW")
                for row_index, attr_element in enumerate(attr_value):
                    text_box = Text(frame_attr, height=1)
                    text_box.grid(row=row_index, column=1, sticky=NSEW)
                    text_box.insert("end", attr_element)
            else:
                frame_attr.rowconfigure(0, weight=100)
                frame_attr.grid(row=attr_index, column=0, sticky=NSEW)
                label_box = Label(frame_attr, height=1, text=f'{attr_name}: '.title())
                label_box.grid(row=0, column=0, sticky="NSW")
                text_box = Text(frame_attr, height=1)
                text_box.grid(row=0, column=1, sticky=NSEW)
                text_box.insert("end", attr_value)
        
        ## Buttons
        btn_save = Button(
            frame_actions,
            text="Save",
            command=self.action_save_edit
        )
        btn_save.grid(
            row=1,
            column=0,
            sticky=NSEW
        )
        btn_cancel = Button(
            frame_actions,
            text="Cancel",
            command=self.action_cancel_edit
        )
        btn_cancel.grid(
            row=1,
            column=1,
            sticky=NSEW
        )
        
        # Calculate popup window geometry
        self.popup_edit.update()
        popup_w = self.popup_edit.winfo_width()
        popup_h = self.popup_edit.winfo_height()
        popup_x = self.root.winfo_screenwidth() // 2 - (popup_w // 2)
        popup_y = self.root.winfo_screenheight() // 2 - (popup_h // 2)
        self.popup_edit.geometry(f'{popup_w}x{popup_h}+{popup_x}+{popup_y}')
        
    def display(self) -> None:
        """Main interface"""
        
        self.table_run.bind("<Button-1>", self.disable_resizing)
        self.table_conf.bind("<Button-1>", self.on_click_config)
        self.table_conf.bind("sel_row")
        self.root.mainloop()
