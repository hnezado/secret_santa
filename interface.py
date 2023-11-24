import os
import json
import logging as log
from tkinter import *
from tkinter import ttk


class Interface:
    def __init__(self, logic, style, input_file) -> None:
        # Main window
        self.root = None
        self.logic = logic
        self.input_file = input_file
        self.dim = {"w": 0, "h": 0}
        self.pos = {"x": 0, "y": 0}
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
        self.table_config_cols = ("family_id", "participant", "age", "exceptions")
        
        # Style fixed settings (since is not modifiable -> hardcoded)
        self.fixed = {
            "win": {
                "minsize": (640, 480),
                "dim": (800, 600),
                "pos": (0, 0)
            },
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
                "padding": 5
            }
        }

        # Data
        self.table_run_data = {}

        # Initialization
        self.set_root()
        self.set_style(style_path=style)
        self.set_tabs()
        
    def set_root(self) -> None:
        """Generates the root window applying its dimensions and position to itself"""
        self.root = Tk()
        self.root.title("Secret Santa")
        self.root.iconbitmap("santa.ico")
        self.root.minsize(self.fixed["win"]["minsize"][0], self.fixed["win"]["minsize"][1])
        
        # Calculate window position (relatively to its dimensions)
        self.fixed["win"]["pos"] = (
            self.root.winfo_screenwidth() // 2 - (self.fixed["win"]["dim"][0] // 2),
            self.root.winfo_screenheight() // 2 - (self.fixed["win"]["dim"][1] // 2),
        )

        # Apply dimensions and position to the window
        self.root.geometry(
            f'{self.fixed["win"]["dim"][0]}x{self.fixed["win"]["dim"][1]}+{self.fixed["win"]["pos"][0]}+{self.fixed["win"]["pos"][1]}'
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
            padding=self.fixed["frame"]["padding"],
            anchor=CENTER
        )
        
        # Notebook
        self.style.configure(
            "TNotebook",
            padding=self.fixed["notebook"]["padding"]
        )

        # Notebook.Tab
        self.style.configure(
            "TNotebook.Tab", 
            padding=self.fixed["notebook.tab"]["padding"],
            font=self.fixed["notebook.tab"]["font"],
            anchor=self.fixed["notebook.tab"]["anchor"]
        )
        
        # Button
        self.style.configure(
            "TButton",
            font=self.fixed["button"]["font"],
            anchor=self.fixed["button"]["anchor"],
        )

        # Treeview
        self.style.configure(
            "Treeview",
            background=self.fixed["treeview"]["background"],
            # fieldbackground=self.fixed["treeview"]["fieldbackground"],
            font=self.fixed["treeview"]["font"],
            # foreground=self.fixed["treeview"]["foreground"],
            rowheight=self.fixed["treeview"]["rowheight"],
        )

        # Treeview.Heading
        self.style.configure(
            "Treeview.Heading",
            # background="#83AF7E",
            font=self.fixed["treeview.heading"]["font"],
            relief=self.fixed["treeview.heading"]["relief"],
            borderwidth=self.fixed["treeview.heading"]["borderwidth"],
            bordercolor=self.fixed["treeview.heading"]["bordercolor"],
            padding=self.fixed["treeview.heading"]["padding"]
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
        self.tab_run = ttk.Frame(self.notebook, padding=self.fixed["frame"]["padding"])
        self.notebook.add(self.tab_run, text="RUN")

        # Buttons
        btn_roll = ttk.Button(self.tab_run, text="Roll", command=self.run, style="Roll.TButton", takefocus=False)
        btn_roll.pack(fill="x", expand=True, pady=(0, 10))
        btn_clear = ttk.Button(self.tab_run, text="Clear", command=self.clear, style="Clear.TButton", takefocus=False)
        btn_clear.pack(fill="x", expand=True, pady=(0, 10))
        
        # Treeview
        self.table_run = ttk.Treeview(self.tab_run, style="Treeview", height=self.fixed["treeview"]["height"])
        self.table_run.configure(columns=self.table_run_cols)
        self.table_run.heading("#0", text="")
        self.table_run.heading("participant", text="Participant", anchor=CENTER)
        self.table_run.heading("assigned", text="Assigned", anchor=CENTER)
        col_width = (self.fixed["win"]["dim"][0] - 2 * (self.fixed["notebook"]["padding"] + self.fixed["frame"]["padding"])) // len(self.table_run_cols)-3
        self.table_run.column("#0", stretch=NO, minwidth=0, width=0)    
        self.table_run.column("participant", stretch=YES, minwidth=10, width=col_width, anchor=CENTER)
        self.table_run.column("assigned", stretch=YES, minwidth=10, width=col_width, anchor=CENTER)    
        
        ## Tag
        self.table_run.tag_configure("oddrow", background="#C7DEB1")

        self.table_run.pack(fill=BOTH, expand=True)
        self.update_tab_run()
        
    def create_tab_config(self):
        """Creates the CONFIGURATION tab"""
        self.tab_config = ttk.Frame(self.notebook, padding=self.fixed["frame"]["padding"])
        self.tab_config.pack(fill="both", expand=True)
        self.notebook.add(self.tab_config, text="CONFIGURATION")

        upd_btn = ttk.Button(self.tab_config, text="Update", command=self.update_tab_config, style="Update.TButton", takefocus=False)
        upd_btn.pack(fill="x", expand=True, pady=(0, 10))
        open_config_btn = ttk.Button(self.tab_config, text="Open configuration file", command=self.open_config_file, style="OpenConfigFile.TButton", takefocus=False)
        open_config_btn.pack(fill="x", expand=True, pady=(0, 10))

        self.table_config = ttk.Treeview(self.tab_config, style="Treeview", height=self.fixed["treeview"]["height"])
        self.table_config.configure(columns=self.table_config_cols)
        self.table_config.heading("#0", text="")
        self.table_config.heading("family_id", text="Family ID", anchor=CENTER)
        self.table_config.heading("participant", text="Participant", anchor=CENTER)
        self.table_config.heading("age", text="Age", anchor=CENTER)
        self.table_config.heading("exceptions", text="Exceptions", anchor=CENTER)
        col_width = (self.fixed["win"]["dim"][0] - 2 * (
                    self.fixed["notebook"]["padding"] + self.fixed["frame"]["padding"])) // len(self.table_config_cols) - 3
        self.table_config.column("#0", stretch=NO, minwidth=0, width=0)
        self.table_config.column("family_id", stretch=YES, minwidth=10, width=col_width, anchor=CENTER)
        self.table_config.column("participant", stretch=YES, minwidth=10, width=col_width, anchor=CENTER)
        self.table_config.column("age", stretch=YES, minwidth=10, width=col_width, anchor=CENTER)
        self.table_config.column("exceptions", stretch=YES, minwidth=10, width=col_width, anchor=CENTER)

        ## Tag
        self.table_config.tag_configure("oddrow", background="#C7DEB1")

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
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            values = (f'{member.family_id}',
                      f'{member.name.title()}',
                      f'{member.age.title()}',
                      f'{", ".join([e.title() for e in member.exceptions])}')
            self.table_config.insert("", "end", values=values, tags=tag)

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
    
    def on_resize(self, _):
        """Updates the window dimensions and position when resized"""
        self.dim = {"w": self.root.winfo_width(), "h": self.root.winfo_height()}
        self.pos = {"x": self.root.winfo_x, "y": self.root.winfo_y}

    @staticmethod
    def disable_resizing(_):
        """Disables the column resizing"""
        return "break"

    def display(self) -> None:
        """Main interface"""
        self.root.bind("<Configure>", self.on_resize)
        self.table_run.bind("<Button-1>", self.disable_resizing)
        self.table_config.bind("<Button-1>", self.disable_resizing)
        self.root.mainloop()
