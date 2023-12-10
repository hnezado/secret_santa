import os
import json
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
        self.tab_run = None
        self.tab_config = None
        self.tab_pref = None
        self.table_run = None
        self.table_config = None
        self.frame_pref_lang = None
        self.label_pref_lang = None
        self.btn_run_roll = None
        self.btn_run_clear = None
        self.btn_pref_lang_en = None
        self.btn_pref_lang_es = None
        self.btn_pref_lang_fr = None

        # Displayed text (language settings)
        self.lang = None
        self.disp_txt = None
        self.update_lang()
        
        # Columns to display in each table
        self.table_run_cols = ("participant", "assigned")
        # self.table_config_cols = ("family_id", "participant", "age", "exceptions")
        self.table_config_cols = ("#0", "family_id", "participant", "age", "exceptions")

        # Root
        self.root = Tk()
        self.fixed_win = {
            "minsize": (640, 480),
            "dim": (800, 600),
            "pos": (0, 0)
        }
        self.set_root()

        # Data
        self.img = {
            "checked": PhotoImage(file='./images/checked.png'),
            "unchecked": PhotoImage(file='./images/unchecked.png')
        }
        self.table_run_data = {}

        # Style
        self.style_static = self.get_style_static()
        self.style_dynamic = self.get_style_dynamic()
        
        # Columns & rows
        self.run_col_width = (self.fixed_win["dim"][0] - 2 * (self.style_static["settings"]["TNotebook"]["configure"]["padding"][0] + self.style_static["settings"]["TFrame"]["configure"]["padding"][0])) // len(self.table_run_cols) - 3
        self.config_first_col_width = 16 * 2 + self.img["checked"].width()
        self.config_col_width = (self.fixed_win["dim"][0] - 2 * (self.style_static["settings"]["TNotebook"]["configure"]["padding"][0]+ + self.style_static["settings"]["TFrame"]["configure"]["padding"][0]) - self.config_first_col_width) // (len(self.table_config_cols) - 1) - 3
        self.table_config_last_index = 0
        
        # Initialization
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
    def get_style_static() -> dict:
        """Retrieves the static style data"""
        with open("./user_settings/styles/static.json") as f:
            static = f.read()
            return json.loads(static)

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
        # self.create_tab_config()
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
            sticky=NSEW
        )
        self.notebook.add(
            self.tab_run
        )

        # Actions frame
        self.frame_run_act = ttk.Frame(
            self.tab_run,
            style="Act.Run.TFrame"
        )

        ## Buttons
        self.btn_run_roll = ttk.Button(
            self.tab_run,
            command=self.run,
            style="Roll.TButton",
            takefocus=False
        )
        self.btn_run_roll.grid(
            row=0,
            column=0
        )
        self.btn_run_clear = ttk.Button(
            self.tab_run,
            command=self.clear,
            style="Clear.TButton",
            takefocus=False
        )
        self.btn_run_clear.grid(
            row=1,
            column=0
        )

        # # Treeview
        # self.table_run = ttk.Treeview(
        #     self.tab_run,
        #     style="Treeview",
        #     height=self.fixed_style["treeview"]["height"]
        # )
        # self.table_run.configure(columns=self.table_run_cols)
        #
        # ## Headings & columns
        # self.table_run.heading(
        #     "#0",
        #     text=""
        # )
        # self.table_run.column(
        #     "#0",
        #     stretch=NO,
        #     minwidth=0,
        #     width=0
        # )
        # for i, v in enumerate(self.table_run_cols):
        #     self.table_run.heading(
        #         v,
        #         text=self.disp_txt["tab_run_table_headings"][i],
        #         anchor=CENTER
        #     )
        #     self.table_run.column(
        #         v,
        #         stretch=YES,
        #         minwidth=self.fixed_style["treeview.column"]["minwidth"],
        #         width=self.run_col_width,
        #         anchor=CENTER
        #     )
        #
        # ## Tags
        # self.table_run.tag_configure(
        #     "oddrow",
        #     background="#C7DEB1"
        # )
        #
        # self.table_run.pack(
        #     fill=BOTH,
        #     expand=True
        # )
        self.update_tab_run()

    def update_tab_run(self) -> None:
        """Updates the RUN tab and its table"""
        self.notebook.tab(self.tab_run, text=self.disp_txt["run"])
        self.btn_run_roll.configure(text=self.disp_txt["btn"]["roll"])
        self.btn_run_clear.configure(text=self.disp_txt["btn"]["clear"])
        # self.empty_table(self.table_run)
        # for i, (name, assigned) in enumerate(self.table_run_data.items()):
        #     tag = "evenrow" if i % 2 == 0 else "oddrow"
        #     values = (f'{name.title()}', f'{", ".join([p.name for p in assigned])}')
        #     self.table_run.insert("", "end", values=values, tags=tag)

    def create_tab_config(self) -> None:
        """Creates the CONFIGURATION tab"""
        # Frame
        self.tab_config = ttk.Frame(
            self.notebook,
            padding=self.fixed_style["frame"]["padding"]
        )
        self.tab_config.pack(
            fill=BOTH,
            expand=True
        )
        self.notebook.add(
            self.tab_config,
            text=self.disp_txt["config"]
        )

        # Buttons
        open_config_btn = ttk.Button(
            self.tab_config,
            text=self.disp_txt["btn"]["open_config_file"],
            command=self.open_config_file,
            style="OpenConfigFile.TButton",
            takefocus=False
        )
        open_config_btn.pack(
            fill=X,
            expand=True,
            pady=self.fixed_style["button"]["generic"]["padding"]
        )
        upd_btn = ttk.Button(
            self.tab_config,
            text=self.disp_txt["btn"]["update_config_table"],
            command=self.update_tab_config,
            style="Update.TButton",
            takefocus=False
        )
        upd_btn.pack(
            fill=X,
            expand=True,
            pady=self.fixed_style["button"]["generic"]["padding"]
        )

        # Treeview
        self.table_config = ttk.Treeview(
            self.tab_config,
            style="Treeview",
            height=self.fixed_style["treeview"]["height"]
        )
        self.table_config.configure(columns=self.table_config_cols[1:])

        ## Headings & columns
        for i, v in enumerate(self.table_config_cols):
            if i == 0:
                self.table_config.heading(
                    v,
                    text=self.disp_txt["tab_config_table_headings"][i],
                    anchor=CENTER
                )
                self.table_config.column(
                    v,
                    stretch=NO,
                    minwidth=self.config_first_col_width,
                    width=self.config_first_col_width
                )
            else:
                self.table_config.heading(
                    v,
                    text=self.disp_txt["tab_config_table_headings"][i],
                    anchor=CENTER
                )
                self.table_config.column(
                    v,
                    stretch=YES,
                    minwidth=self.fixed_style["treeview.column"]["minwidth"], 
                    width=self.config_col_width,
                    anchor=CENTER
                )
        
        ## Tags
        self.table_config.tag_configure(
            "oddrow",
            background="#C7DEB1"
        )

        self.table_config.pack(
            fill=BOTH,
            expand=True
        )
        self.update_tab_config()

    def update_tab_config(self) -> None:
        """Updates the CONFIGURATION tab and its table"""
        self.empty_table(self.table_config)
        self.logic.read_participants()
        self.logic.parse_participants()
        for i, member in enumerate(self.logic.participants.values()):
            tags = ("evenrow" if i % 2 == 0 else "oddrow")
            img = self.img["checked"] if member.enabled else self.img["unchecked"]
            values = (f'{member.family_id}',
                      f'{member.name.title()}',
                      f'{member.age.title()}',
                      f'{", ".join([e.title() for e in member.exceptions])}')
            if "enabled" in tags:
                self.table_config.insert(
                    "",
                    "end",
                    id=self.table_config_last_index,
                    image=img,
                    values=values,
                    tags=tags
                )
            else:
                self.table_config.insert(
                    "", 
                    "end",
                    id=self.table_config_last_index,
                    image=img,
                    values=values,
                    tags=tags
                )
            self.table_config_last_index += 1

    def create_tab_pref(self) -> None:
        """Creates de PREFERENCES tab"""
        # Frame
        self.tab_pref = ttk.Frame(
            self.notebook,
            style="Pref.TFrame"
        )
        self.tab_pref.rowconfigure(0, weight=50)
        self.tab_pref.rowconfigure(1, weight=50)
        self.tab_pref.columnconfigure(0, weight=100)

        self.tab_pref.grid(
            row=0,
            column=0,
            sticky=NSEW
        )
        self.notebook.add(
            self.tab_pref
        )
        
        # Language preferences frame
        self.frame_pref_lang = ttk.Frame(
            self.tab_pref,
            style="Lang.Pref.TFrame"
        )
        self.frame_pref_lang.rowconfigure(0, weight=50)
        self.frame_pref_lang.rowconfigure(1, weight=50)
        self.frame_pref_lang.columnconfigure(0, weight=33)
        self.frame_pref_lang.columnconfigure(1, weight=33)
        self.frame_pref_lang.columnconfigure(2, weight=33)
        self.frame_pref_lang.grid(
            row=0,
            column=0,
            sticky=NSEW
        )
        # Language label
        self.label_pref_lang = ttk.Label(
            self.frame_pref_lang,
            style="Lang.Pref.TLabel"
        )
        self.label_pref_lang.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky=NSEW
        )
        
        ## Buttons language
        self.btn_pref_lang_en = ttk.Button(
            self.frame_pref_lang,
            command=self.swap_lang_en,
            style="Lang.TButton",
            takefocus=False
        )
        self.btn_pref_lang_en.grid(
            row=1,
            column=0
        )
        self.btn_pref_lang_es = ttk.Button(
            self.frame_pref_lang,
            command=self.swap_lang_es,
            style="Lang.TButton",
            takefocus=False
        )
        self.btn_pref_lang_es.grid(
            row=1,
            column=1
        )
        self.btn_pref_lang_fr = ttk.Button(
            self.frame_pref_lang,
            command=self.swap_lang_fr,
            style="Lang.TButton",
            takefocus=False
        )
        self.btn_pref_lang_fr.grid(
            row=1,
            column=2
        )
        
        self.update_tab_pref()

    def update_tab_pref(self) -> None:
        """Updates the PREFERENCES tab"""
        self.notebook.tab(self.tab_pref, text=self.disp_txt["pref"])
        self.label_pref_lang.configure(text=self.disp_txt["label"]["lang"])
        self.btn_pref_lang_en.configure(text=self.disp_txt["btn"]["lang_en"])
        self.btn_pref_lang_es.configure(text=self.disp_txt["btn"]["lang_es"])
        self.btn_pref_lang_fr.configure(text=self.disp_txt["btn"]["lang_fr"])
        
        # Buttons
        # btn_pref_future = ttk.Button(
        #     self.tab_pref,
        #     text=self.disp_txt["btn"]["future_impl"],
        #     command=None,
        #     style="TButton",
        #     takefocus=False
        # )
        # btn_pref_future.grid(
        #     row=1,
        #     column=0,
        #     # pady=self.fixed_style["button"]["generic"]["padding"],
        # )

    def empty_table(self, table: ttk.Treeview) -> None:
        """Empties the config table and resets its index"""
        table.delete(*table.get_children())
        self.table_config_last_index = 0

    def run(self) -> None:
        """Retrieves the randomized paired data"""
        self.table_run_data = self.logic.run()
        self.update_tab_run()

    def clear(self) -> None:
        """Clears the retrieved data and the treeview"""
        self.table_run_data.clear()
        self.update_tab_run()

    def open_config_file(self) -> None:
        """Opens the configuration file to edit it"""
        os.system("notepad.exe " + self.uset.user_settings["input_file"])

    def swap_check(self, row: int) -> None:
        """Swaps the member status (enabled, disabled)"""
        member = list(self.logic.participants.keys())[row]
        self.logic.participants[member].enabled = not self.logic.participants[member].enabled

    def swap_lang_en(self) -> None:
        self.update_lang("en")
        self.update_tab_run()
        # self.update_tab_config()
        self.update_tab_pref()
    
    def swap_lang_es(self) -> None:
        self.update_lang("es")
        self.update_tab_run()
        # self.update_tab_config()
        self.update_tab_pref()
    
    def swap_lang_fr(self) -> None:
        self.update_lang("fr")
        self.update_tab_run()
        # self.update_tab_config()
        self.update_tab_pref()

    @staticmethod
    def disable_resizing(_) -> str:
        """Disables the column resizing"""
        return "break"

    def on_click_config(self, event: Event) -> str | None:
        """Called on click event"""
        region = self.table_config.identify("region", event.x, event.y)
        if region == "separator":
            return self.disable_resizing(event)
        elif region == "tree" or region == "cell":
            try:
                row = int(self.table_config.identify_row(event.y))
                col = int(self.table_config.identify_column(event.x)[1:])
                if col == 0:
                    self.swap_check(row)
                    self.logic.update_config_file()
                    self.update_tab_config()
            except:
                log.error("Cell coordinates cannot be calculated")

    def display(self) -> None:
        """Main interface"""
        # self.table_run.bind("<Button-1>", self.disable_resizing)
        # self.table_config.bind("<Button-1>", self.on_click_config)
        self.root.mainloop()
