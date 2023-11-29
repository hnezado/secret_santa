import os
import json
import logging as log
from tkinter import *
from tkinter import ttk


class Interface:
    def __init__(self, logic, settings) -> None:
        # Main
        self.logic = logic
        self.lang = settings["lang"]
        self.input_file = settings["input_file"]
        self.style = None

        # Components
        self.notebook = None
        self.tab_run = None
        self.tab_config = None
        self.tab_pref = None
        self.table_run = None
        self.table_config = None
        self.scroll_bar_run = None
        self.table_config_last_index = 0

        # Displayed text (language settings)
        self.disp_txt = None
        self.set_lang()
        
        # Columns to display in each table
        self.table_run_cols = ("participant", "assigned")
        # self.table_config_cols = ("family_id", "participant", "age", "exceptions")
        self.table_config_cols = ("#0", "family_id", "participant", "age", "exceptions")

        # Root
        self.root = None
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
        self.fixed_style = {
            "frame": {
                "padding": 10
            },
            "notebook": {
                "padding": 10
            },
            "notebook.tab": {
                "padding": (49, 10),
                "font": ("Calibri", 16, "bold"),
                "anchor": CENTER
            },
            "button": {
                "font": ("Calibri", 32),
                "anchor": CENTER,
                "padding": (0, 10),
            },
            "treeview": {
                # "background": "#E0F7CB",
                "background": "#E1E1E1",
                # "fieldbackground": "#EEFAE3",
                "font": ("Calibri", 10),
                # "foreground": "#173D1E",
                "rowheight":20,
                "height": 256,
                "borderwidth": 5
            },
            "treeview.heading": {
                # "background": "#83AF7E",
                "font": ("Calibri", 12, "bold"),
                "relief": "solid", # ["solid", "groove"]
                "borderwidth": 1,
                "bordercolor": "#173D1E",
                "padding": (0, 10)
            },
            "treeview.column": {
                "minwidth": 10
            }
        }
        
        # Columns
        self.run_col_width = (self.fixed_win["dim"][0] - 2 * (self.fixed_style["notebook"]["padding"] + self.fixed_style["frame"]["padding"])) // len(self.table_run_cols)-3
        self.config_first_col_width = 16 * 2 + self.img["checked"].width()
        # self.config_col_width = (self.fixed_win["dim"][0] - 2 * (self.fixed_style["notebook"]["padding"] + self.fixed_style["frame"]["padding"]) - self.config_first_col_width) // len(self.table_config_cols) - 3
        self.config_col_width = (self.fixed_win["dim"][0] - 2 * (self.fixed_style["notebook"]["padding"] + self.fixed_style["frame"]["padding"]) - self.config_first_col_width) // (len(self.table_config_cols)-1) - 3
        print(self.config_col_width)
        
        # Initialization
        self.set_style(style_path=settings["style"])
        self.set_tabs()

    def set_lang(self) -> None:
        """Sets the selected language"""
        with open("./settings/lang.json") as f:
            raw = f.read()
            self.disp_txt = json.loads(raw)[self.lang]

    def set_root(self) -> None:
        """Generates the root window with its dimensions and position"""
        self.root = Tk()
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

    def set_style(self, style_path: str) -> ttk.Style:
        """Creates a new passed style if not create already"""
        # Style data import
        self.style = ttk.Style()
        with open(style_path) as f:
            j = f.read()
            style_content = json.loads(j)
            
        # Style creation
        try:
            self.style.theme_create(**style_content)
        except:
            log.info(f'Theme {style_content["themename"]} already exists')
        
        # Style application
        self.style.theme_use(style_content["themename"])
        self.update_style()

    def update_style(self) -> None:
        """Updates the style with un-mutable settings"""
        # Frame
        self.style.configure(
            "TFrame",
            padding=self.fixed_style["frame"]["padding"],
            anchor=CENTER
        )

        # Notebook
        self.style.configure(
            "TNotebook",
            padding=self.fixed_style["notebook"]["padding"]
        )

        # Notebook.Tab
        self.style.configure(
            "TNotebook.Tab",
            padding=self.fixed_style["notebook.tab"]["padding"],
            font=self.fixed_style["notebook.tab"]["font"],
            anchor=self.fixed_style["notebook.tab"]["anchor"]
        )

        # Button
        self.style.configure(
            "TButton",
            font=self.fixed_style["button"]["font"],
            anchor=self.fixed_style["button"]["anchor"],
        )

        # Treeview
        self.style.configure(
            "Treeview",
            background=self.fixed_style["treeview"]["background"],
            # fieldbackground=self.fixed_style["treeview"]["fieldbackground"],
            font=self.fixed_style["treeview"]["font"],
            # foreground=self.fixed_style["treeview"]["foreground"],
            rowheight=self.fixed_style["treeview"]["rowheight"],
        )

        # Treeview.Heading
        self.style.configure(
            "Treeview.Heading",
            # background="#83AF7E",
            font=self.fixed_style["treeview.heading"]["font"],
            relief=self.fixed_style["treeview.heading"]["relief"],
            borderwidth=self.fixed_style["treeview.heading"]["borderwidth"],
            bordercolor=self.fixed_style["treeview.heading"]["bordercolor"],
            padding=self.fixed_style["treeview.heading"]["padding"]
        )

    def set_tabs(self):
        """Set the notebook and its tabs"""
        self.notebook = ttk.Notebook(self.root)
        self.create_tab_run()
        self.create_tab_config()
        self.create_tab_pref()
        self.notebook.pack(
            fill=BOTH,
            expand=True
        )

    def create_tab_run(self):
        """Creates the RUN tab"""
        # TFrame
        self.tab_run = ttk.Frame(
            self.notebook,
            padding=self.fixed_style["frame"]["padding"]
        )
        self.notebook.add(
            self.tab_run,
            text=self.disp_txt["run"]
        )

        # Buttons
        btn_roll = ttk.Button(
            self.tab_run,
            text=self.disp_txt["but"]["roll"],
            command=self.run,
            style="Roll.TButton",
            takefocus=False
        )
        btn_roll.pack(
            fill=X,
            expand=True,
            pady=self.fixed_style["button"]["padding"]
        )
        btn_clear = ttk.Button(
            self.tab_run,
            text=self.disp_txt["but"]["clear"], 
            command=self.clear,
            style="Clear.TButton",
            takefocus=False
        )
        btn_clear.pack(
            fill=X,
            expand=True,
            pady=self.fixed_style["button"]["padding"]
        )

        # Treeview
        self.table_run = ttk.Treeview(
            self.tab_run,
            style="Treeview",
            height=self.fixed_style["treeview"]["height"]
        )
        self.table_run.configure(columns=self.table_run_cols)
        
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
                minwidth=self.fixed_style["treeview.column"]["minwidth"],
                width=self.run_col_width,
                anchor=CENTER
            )

        ## Tags
        self.table_run.tag_configure(
            "oddrow",
            background="#C7DEB1"
        )

        self.table_run.pack(
            fill=BOTH,
            expand=True
        )
        self.update_tab_run()

    def update_tab_run(self):
        """Updates the RUN tab and its table"""
        self.empty_table(self.table_run)
        for i, (name, assigned) in enumerate(self.table_run_data.items()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            values = (f'{name.title()}', f'{", ".join([p.name for p in assigned])}')
            self.table_run.insert("", "end", values=values, tags=tag)

    def create_tab_config(self):
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
            text=self.disp_txt["but"]["open_config_file"],
            command=self.open_config_file,
            style="OpenConfigFile.TButton",
            takefocus=False
        )
        open_config_btn.pack(
            fill=X,
            expand=True,
            pady=self.fixed_style["button"]["padding"]
        )
        upd_btn = ttk.Button(
            self.tab_config,
            text=self.disp_txt["but"]["update_config_table"],
            command=self.update_tab_config,
            style="Update.TButton",
            takefocus=False
        )
        upd_btn.pack(
            fill=X,
            expand=True,
            pady=self.fixed_style["button"]["padding"]
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

    def update_tab_config(self):
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

    def create_tab_pref(self):
        """Creates de PREFERENCES tab"""
        # Frame
        self.tab_pref = ttk.Frame(
            self.notebook,
            style="TFrame",
            padding=self.fixed_style["frame"]["padding"]
        )
        self.tab_pref.pack(
            fill=BOTH,
            expand=True
            )
        self.notebook.add(
            self.tab_pref,
            text=self.disp_txt["pref"]
        )
        
        # Buttons
        open_pref_btn = ttk.Button(
            self.tab_pref,
            text=self.disp_txt["but"]["future_impl"],
            command=None,
            style="OpenPrefFile.TButton",
            takefocus=False
        )
        open_pref_btn.pack(
            fill=BOTH,
            expand=True,
            pady=self.fixed_style["button"]["padding"],
        )

    def empty_table(self, table):
        """Empties the config table and resets its index"""
        table.delete(*table.get_children())
        self.table_config_last_index = 0

    def run(self):
        """Retrieves the randomized paired data"""
        self.table_run_data = self.logic.run()
        self.update_tab_run()

    def clear(self):
        """Clears the retrieved data and the treeview"""
        self.table_run_data.clear()
        self.update_tab_run()

    def open_config_file(self):
        """Opens the configuration file to edit it"""
        os.system("notepad.exe " + self.input_file)

    def swap_check(self, row) -> None:
        """Swaps the member status (enabled, disabled)"""
        member = list(self.logic.participants.keys())[row]
        self.logic.participants[member].enabled = not self.logic.participants[member].enabled

    @staticmethod
    def disable_resizing(_):
        """Disables the column resizing"""
        return "break"

    def on_click_config(self, event):
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
        self.table_run.bind("<Button-1>", self.disable_resizing)
        self.table_config.bind("<Button-1>", self.on_click_config)
        self.root.mainloop()
