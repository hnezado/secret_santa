import os
import json
import logging as log
from tkinter import *
from tkinter import ttk


class Interface:
    def __init__(self, logic, style, input_file) -> None:
        # Main
        self.logic = logic
        self.input_file = input_file
        self.style = None

        # Components
        self.notebook = None
        self.tab_run = None
        self.tab_config = None
        self.tab_pref = None
        self.table_run = None
        self.table_config = None
        self.scroll_bar_run = None
        self.table_config_last_index = 1

        # Columns to display in each table
        self.table_run_cols = ("participant", "assigned")
        self.table_config_cols = ("family_id", "participant", "age", "exceptions")

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
            }
        }
        
        # Columns
        self.run_col_width = (self.fixed_win["dim"][0] - 2 * (self.fixed_style["notebook"]["padding"] + self.fixed_style["frame"]["padding"])) // len(self.table_run_cols)-3
        self.config_first_col_width = 16 * 2 + self.img["checked"].width()
        self.config_col_width = (self.fixed_win["dim"][0] - 2 * (self.fixed_style["notebook"]["padding"] + self.fixed_style["frame"]["padding"]) - self.config_first_col_width) // len(self.table_config_cols) - 3
        
        # Initialization
        self.set_style(style_path=style)
        self.set_tabs()

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
            text="RUN"
        )

        # Buttons
        btn_roll = ttk.Button(
            self.tab_run,
            text="Roll",
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
            text="Clear", 
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
        
        ## Headings
        self.table_run.heading(
            "#0",
            text=""
        )
        self.table_run.heading(
            "participant",
            text="Participant",
            anchor=CENTER
        )
        self.table_run.heading(
            "assigned",
            text="Assigned",
            anchor=CENTER
        )
        
        ## Columns
        self.table_run.column(
            "#0",
            stretch=NO,
            minwidth=0,
            width=0
        )
        self.table_run.column(
            "participant",
            stretch=YES,
            minwidth=10,
            width=self.run_col_width,
            anchor=CENTER
        )
        self.table_run.column(
            "assigned",
            stretch=YES,
            minwidth=10,
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
            text="CONFIGURATION"
        )

        # Buttons
        open_config_btn = ttk.Button(
            self.tab_config,
            text="Open configuration file",
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
            text="Update table from file",
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
        self.table_config.configure(columns=self.table_config_cols)

        ## Headings
        self.table_config.heading(
            "#0",
            text="Status",
            anchor=CENTER
        )
        self.table_config.heading(
            "family_id",
            text="Family ID",
            anchor=CENTER
        )
        self.table_config.heading(
            "participant",
            text="Participant",
            anchor=CENTER
        )
        self.table_config.heading(
            "age",
            text="Age",
            anchor=CENTER
        )
        self.table_config.heading(
            "exceptions",
            text="Exceptions",
            anchor=CENTER
        )

        ## Columns
        self.table_config.column(
            "#0",
            stretch=NO,
            minwidth=self.config_first_col_width,
            width=self.config_first_col_width
        )
        self.table_config.column(
            "family_id",
            stretch=YES,
            minwidth=10, 
            width=self.config_col_width,
            anchor=CENTER
        )
        self.table_config.column(
            "participant",
            stretch=YES, 
            minwidth=10,
            width=self.config_col_width,
            anchor=CENTER
        )
        self.table_config.column(
            "age",
            stretch=YES, 
            minwidth=10,
            width=self.config_col_width,
            anchor=CENTER
        )
        self.table_config.column(
            "exceptions",
            stretch=YES,
            minwidth=10,
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

    def create_tab_pref(self):
        """Creates de PREFERENCES tab"""
        # Frame
        self.tab_pref = ttk.Frame(
            self.notebook,
            style="TFrame",
            padding=20
        )
        self.tab_pref.pack(
            fill=BOTH,
            expand=True
            )
        self.notebook.add(
            self.tab_pref,
            text="PREFERENCES"
        )
        
        # Buttons
        open_pref_btn = ttk.Button(
            self.tab_pref,
            text="Customizable\nfuture implementations",
            command=None,
            style="OpenPrefFile.TButton",
            takefocus=False
        )
        open_pref_btn.pack(
            fill=BOTH,
            expand=True,
            pady=self.fixed_style["button"]["padding"],
        )

    def update_tab_run(self):
        """Updates the RUN tab"""
        self.empty_table(self.table_run)
        for i, (name, assigned) in enumerate(self.table_run_data.items()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            values = (f'{name.title()}', f'{", ".join([p.name for p in assigned])}')
            self.table_run.insert("", "end", values=values, tags=tag)

    def update_tab_config(self):
        """Updates the CONFIGURATION tab"""
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

    def empty_table(self, table):
        """Empties the config table and resets its index"""
        table.delete(*table.get_children())
        self.table_config_last_index = 1

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
        member = list(self.logic.participants.keys())[row-1]
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
                col = int(self.table_config.identify_column(event.x)[1:])+1
                if col == 1:
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
