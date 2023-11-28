import os
import json
import logging as log
from tkinter import *
from tkinter import ttk


class Interface:
    def __init__(self, logic, style, input_file) -> None:
        # Main window
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

        # Columns to display in each table
        self.table_run_cols = ("participant", "assigned")
        # self.table_config_cols = ("enabled", "family_id", "participant", "age", "exceptions")
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
                "anchor": CENTER
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
                "padding": (0, 0)
            }
        }
        self.first_col_width = 16 * 2 + self.img["checked"].width()
        self.col_width = (self.fixed_win["dim"][0] - 2 * (self.fixed_style["notebook"]["padding"] + self.fixed_style["frame"]["padding"]) - self.first_col_width) // len(self.table_config_cols) - 3
        
        self.set_style(style_path=style)
        self.set_tabs()

    def set_root(self) -> None:
        """Generates the root window applying its dimensions and position to itself"""
        self.root = Tk()
        self.root.title("Secret Santa")
        self.root.iconbitmap("santa.ico")
        self.root.minsize(self.fixed_win["minsize"][0], self.fixed_win["minsize"][1])

        # Calculate window position (relatively to its dimensions)
        self.fixed_win["pos"] = (
            self.root.winfo_screenwidth() // 2 - (self.fixed_win["dim"][0] // 2),
            self.root.winfo_screenheight() // 2 - (self.fixed_win["dim"][1] // 2),
        )

        # Apply dimensions and position to the window
        self.root.geometry(
            f'{self.fixed_win["dim"][0]}x{self.fixed_win["dim"][1]}+{self.fixed_win["pos"][0]}+{self.fixed_win["pos"][1]}'
        )

    def set_style(self, style_path) -> ttk.Style:
        """Creates a new passed style if not create already"""
        self.style = ttk.Style()
        with open(style_path) as f:
            j = f.read()
            style_content = json.loads(j)

        try:
            self.style.theme_create(**style_content)
        except:
            log.info(f'Theme {style_content["themename"]} already exists')
        self.style.theme_use(style_content["themename"])
        self.update_style()

    def update_style(self):
        """Updates the style with the un-mutable settings"""
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
        """Set notebook and each of its tab"""
        self.notebook = ttk.Notebook(self.root)
        self.create_tab_run()
        self.create_tab_config()
        self.create_tab_pref()
        self.notebook.pack(fill=BOTH, expand=True)

    def create_tab_run(self):
        """Creates the RUN tab"""
        # TFrame
        self.tab_run = ttk.Frame(self.notebook, padding=self.fixed_style["frame"]["padding"])
        self.notebook.add(self.tab_run, text="RUN")

        # Buttons
        btn_roll = ttk.Button(self.tab_run, text="Roll", command=self.run, style="Roll.TButton", takefocus=False)
        btn_roll.pack(fill="x", expand=True, pady=(0, 10))
        btn_clear = ttk.Button(self.tab_run, text="Clear", command=self.clear, style="Clear.TButton", takefocus=False)
        btn_clear.pack(fill="x", expand=True, pady=(0, 10))

        # Treeview
        self.table_run = ttk.Treeview(self.tab_run, style="Treeview", height=self.fixed_style["treeview"]["height"])
        self.table_run.configure(columns=self.table_run_cols)
        self.table_run.heading("#0", text="")
        self.table_run.heading("participant", text="Participant", anchor=CENTER)
        self.table_run.heading("assigned", text="Assigned", anchor=CENTER)
        col_width = (self.fixed_win["dim"][0] - 2 * (self.fixed_style["notebook"]["padding"] + self.fixed_style["frame"]["padding"])) // len(self.table_run_cols)-3
        self.table_run.column("#0", stretch=NO, minwidth=0, width=0)
        self.table_run.column("participant", stretch=YES, minwidth=10, width=col_width, anchor=CENTER)
        self.table_run.column("assigned", stretch=YES, minwidth=10, width=col_width, anchor=CENTER)

        ## Tag
        self.table_run.tag_configure("oddrow", background="#C7DEB1")

        self.table_run.pack(fill=BOTH, expand=True)
        self.update_tab_run()

    def create_tab_config(self):
        """Creates the CONFIGURATION tab"""
        # Notebook
        self.tab_config = ttk.Frame(self.notebook, padding=self.fixed_style["frame"]["padding"])
        self.tab_config.pack(fill="both", expand=True)
        self.notebook.add(self.tab_config, text="CONFIGURATION")

        # Buttons
        upd_btn = ttk.Button(self.tab_config, text="Update", command=self.update_tab_config, style="Update.TButton", takefocus=False)
        upd_btn.pack(fill="x", expand=True, pady=(0, 10))
        open_config_btn = ttk.Button(self.tab_config, text="Open configuration file", command=self.open_config_file, style="OpenConfigFile.TButton", takefocus=False)
        open_config_btn.pack(fill="x", expand=True, pady=(0, 10))

        # Treeview
        self.table_config = ttk.Treeview(self.tab_config, style="Treeview", height=self.fixed_style["treeview"]["height"])
        self.table_config.configure(columns=self.table_config_cols)

        ## Headings
        self.table_config.heading("#0", text="Status", anchor=CENTER)
        self.table_config.heading("family_id", text="Family ID", anchor=CENTER)
        self.table_config.heading("participant", text="Participant", anchor=CENTER)
        self.table_config.heading("age", text="Age", anchor=CENTER)
        self.table_config.heading("exceptions", text="Exceptions", anchor=CENTER)

        ## Columns
        self.table_config.column("#0", stretch=NO, minwidth=self.first_col_width, width=self.first_col_width)
        self.table_config.column("family_id", stretch=YES, minwidth=10, width=self.col_width, anchor=CENTER)
        self.table_config.column("participant", stretch=YES, minwidth=10, width=self.col_width, anchor=CENTER)
        self.table_config.column("age", stretch=YES, minwidth=10, width=self.col_width, anchor=CENTER)
        self.table_config.column("exceptions", stretch=YES, minwidth=10, width=self.col_width, anchor=CENTER)
        
        ## Tag
        self.table_config.tag_configure("oddrow", background="#C7DEB1")
        self.table_config.tag_configure("enabled", image=self.img["checked"])
        self.table_config.tag_configure("disabled", image=self.img["unchecked"])

        self.table_config.pack(fill=BOTH, expand=True)
        self.update_tab_config()

    def create_tab_pref(self):
        """Creates de PREFERENCES tab"""
        self.tab_pref = ttk.Frame(self.notebook, style="TFrame", padding=20)
        self.tab_pref.pack(fill="both", expand=True)
        self.notebook.add(self.tab_pref, text="PREFERENCES")

    def update_tab_run(self):
        """Updates the RUN tab"""
        self.table_run.delete(*self.table_run.get_children())

        for i, (name, assigned) in enumerate(self.table_run_data.items()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            values = (f'{name.title()}', f'{", ".join([p.name for p in assigned])}')
            self.table_run.insert("", "end", values=values, tags=tag)

    def update_tab_config(self):
        self.table_config.delete(*self.table_config.get_children())
        self.logic.read_participants()
        for i, member in enumerate(self.logic.participants.values()):
            tags = []
            tags.append("evenrow") if i % 2 == 0 else tags.append("oddrow")
            tags.append("enabled") if member.enabled else tags.append("disabled")
            # tags = "evenrow" if i % 2 == 0 else "oddrow"
            img = self.img["checked"] if member.enabled else self.img["unchecked"]
            values = (f'{member.family_id}',
                      f'{member.name.title()}',
                      f'{member.age.title()}',
                      f'{", ".join([e.title() for e in member.exceptions])}')
            if "enabled" in tags:
                self.table_config.insert("", "end", image=img, values=values, tags=tags)
            else:
                self.table_config.insert("", "end", image=img, values=values, tags=tags)

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

    @staticmethod
    def disable_resizing(_):
        """Disables the column resizing"""
        return "break"

    def on_click_config(self, event):
        region = self.table_config.identify("region", event.x, event.y)
        if region == "separator":
            return self.disable_resizing(event)
        elif region == "tree" or region == "cell":
            try:
                row = int(self.table_config.identify_row(event.y)[1:], 16)
                col = int(self.table_config.identify_column(event.x)[1:], 16)+1
            except:
                log.error("Cell coordinates cannot be calculated")
            print((row, col))
            if col == 1:
                self.swap_check(row)

    def display(self) -> None:
        """Main interface"""
        # self.root.bind("<Configure>", self.on_resize)
        self.table_run.bind("<Button-1>", self.disable_resizing)
        self.table_config.bind("<Button-1>", self.on_click_config)
        self.root.mainloop()
