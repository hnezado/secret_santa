import json
import datetime as dt
import logging as log
from tkinter import *
from tkinter import ttk

# Logging configuration
log.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f'./logs/{dt.datetime.now().strftime("%Y-%m-%d")}.log', 
    level=log.INFO)

class Interface:
    def __init__(self, style, logic) -> None:
        # Main window
        self.root = None
        self.dim = {"w": 0, "h": 0}
        self.pos = {"x": 0, "y": 0}
        self.run = logic[0]
        self.clear = logic[1]
        self.style = None
        
        # Components
        self.notebook = None
        self.tab_run = None
        self.tab_config = None
        self.tab_pref = None
        self.table_run = None
        self.scroll_bar_run = None
        
        # Columns to display in each table
        self.table_run_cols = ("participant", "assigned")
        self.table_config_cols = ("family_id", "participant", "age", "except")
        
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
            "tab": {
                "padding": (49,10)
            },
            "treeview": {
                "height": 256,
                "borderwidth": 5
            }
        }
        
        # Initialization
        self.set_root()
        self.set_style(style_path=style)
        self.set_tabs()
        
    def set_root(self) -> None:
        """Generates the root window applying its dimensions and position to itself
        """
        
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
        # Frame
        self.style.configure(
            "TFrame",
            padding=self.fixed["frame"]["padding"]
        )
        
        # Notebook
        self.style.configure(
            "TNotebook",
            padding=self.fixed["notebook"]["padding"]
        )

        # Notebook.Tab
        self.style.configure(
            "TNotebook.Tab", 
            padding=self.fixed["tab"]["padding"],
            font=("Calibri", 16, "bold"),
            anchor="center"
        )

        # Treeview
        self.style.configure(
            "Treeview",
            foreground="#F56AA4",
            font=("Calibri", 10),
            anchor="w"
            # evenoddrowcolors=[("#E0F7CB", "#B1D2A3")],
            # relief="groove")
        )

        # Treeview.Heading
        self.style.configure(
            "Treeview.Heading",
            font=("Calibri", 12, "bold"),
            borderwidth=1,
            bordercolor="#ad34c4",
            relief="solid",
            highlightbackground="#E03A20",
            padding=10
            # relief="groove")
        )
        
        # Table headings
        # table_headings_config = {
        #     # "anchor": "center",
        #     # "borderwidth": 5,
        #     # "relief": "groove"
        # }
    
    def set_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.create_tab_run()
        self.create_tab_config()
        self.create_tab_pref()
        self.notebook.pack(fill=BOTH, expand=True)
    
    def create_tab_run(self):
        # TFrame
        self.tab_run = ttk.Frame(self.notebook, padding=self.fixed["frame"]["padding"])
        self.notebook.add(self.tab_run, text="RUN")

        # Buttons
        btn_roll = ttk.Button(self.tab_run, text="Roll", command=self.run, style="Roll.TButton")
        btn_roll.pack(fill="x", expand=True, pady=(0, 10))
        btn_clear = ttk.Button(self.tab_run, text="Clear", command=self.clear, style="Clear.TButton")
        btn_clear.pack(fill="x", expand=True, pady=(0, 10))
        
        # Treeview
        self.table_run = ttk.Treeview(self.tab_run, style="Treeview", height=self.fixed["treeview"]["height"])
        self.table_run.configure(columns=self.table_run_cols)
        self.table_run.tag_configure("even_row", background="#B1D2A3")    
        self.table_run.heading("#0", text="")
        self.table_run.heading("participant", text="Participant", anchor=CENTER)
        self.table_run.heading("assigned", text="Assigned", anchor=CENTER)

        col_width = (self.fixed["win"]["dim"][0] - 2 * (self.fixed["notebook"]["padding"] + self.fixed["frame"]["padding"])) // len(self.table_run_cols)-2
        self.table_run.column("#0", stretch=NO, minwidth=0, width=0)    
        self.table_run.column("participant", stretch=NO, minwidth=10, width=col_width, anchor=CENTER)
        self.table_run.column("assigned", stretch=NO, minwidth=10, width=col_width, anchor=CENTER)    
    
        self.table_run.insert("", "end", text="1", values=("John", 30))
        self.table_run.insert("", "end", text="2", values=("Alice", 25))
        self.table_run.insert("", "end", text="3", values=("John", 20))
        self.table_run.insert("", "end", text="4", values=("Alex", 19))
        self.table_run.insert("", "end", text="5", values=("Erika", 27))
        self.table_run.insert("", "end", text="6", values=("Matt", 38))
        self.table_run.insert("", "end", text="7", values=("Natasha", 24))
        self.table_run.insert("", "end", text="8", values=("Rudy", 22))
        self.table_run.insert("", "end", text="9", values=("Helen", 32))
        self.table_run.insert("", "end", text="10", values=("Gary", 34))
        self.table_run.insert("", "end", text="11", values=("Mary", 21))
        self.table_run.insert("", "end", text="12", values=("Jimmy", 40))
        self.table_run.insert("", "end", text="13", values=("Tracy", 46))
        self.table_run.insert("", "end", text="14", values=("Ben", 18))
        self.table_run.insert("", "end", text="15", values=("Anne", 42))
        self.table_run.insert("", "end", text="16", values=("Phil", 33))
        self.table_run.insert("", "end", text="17", values=("Andrew", 26))
        self.table_run.insert("", "end", text="18", values=("Christine", 28))
        self.table_run.insert("", "end", text="19", values=("Amanda", 21))
        self.table_run.insert("", "end", text="20", values=("Lucy", 31))

        self.table_run.pack(fill=BOTH, expand=True)
        
        # # Scrollbar
        # self.scroll_bar_run = Scrollbar(self.tab_run, orient="vertical")
        # self.table_run.config(yscrollcommand=self.scroll_bar_run.set)
        # self.scroll_bar_run.pack(side=RIGHT, fill=Y)
        
    def create_tab_config(self):
        self.tab_config = ttk.Frame(self.notebook, style="TFrame", padding=20)
        self.tab_config.pack(fill="both", expand=True)
        self.notebook.add(self.tab_config, text="CONFIGURATION")

        # self.table_config = ttk.Treeview(self.tab_config, padding=5, height=18)
        # self.table_config["columns"] = ("family_id", "participant", "age", "except")
        # self.table_config.column("#0", width=0, stretch=tk.NO)
        # self.table_config.tag_configure("even_row", background="#B1D2A3")
        # self.table_config.heading("family_id", text="Family ID", anchor="center")
        # self.table_config.heading("participant", text="Participant", anchor="center")
        # self.table_config.heading("age", text="Age", anchor="center")
        # self.table_config.heading("except", text="Exceptions", anchor="center")
        # self.table_config.grid(column=0, row=0, pady=(20, 0), sticky="nswe")

        # upd_btn = ttk.Button(self.tab_config, text="Update", command=self.update_config, style="Update.TButton")
        # upd_btn.grid(column=0, row=1, pady=(10, 0))
        # open_config_btn = ttk.Button(self.tab_config, text="Open configuration file", command=self.open_config, style="OpenConfig.TButton")
        # open_config_btn.grid(column=0, row=2, pady=(20, 0))

        # self.update_config()
    
    def create_tab_pref(self):
        self.tab_pref = ttk.Frame(self.notebook, style="TFrame", padding=20)
        self.tab_pref.pack(fill="both", expand=True)
        self.notebook.add(self.tab_pref, text="PREFERENCES")
    
    def display(self) -> None:
        self.root.bind("<Configure>", self.on_resize)
        self.root.mainloop()
        
    def on_resize(self, _):
        self.dim = {"w": self.root.winfo_width(), "h": self.root.winfo_height()}
        self.pos = {"x": self.root.winfo_x, "y": self.root.winfo_y}

