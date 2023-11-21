import json
from tkinter import *
from tkinter import ttk


class Interface:
    def __init__(self, style, logic) -> None:
        # Main window
        self.root = Tk()
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
        
        # Initialization
        # self.set_root()
        # self.set_style(style_name=style)
        self.set_tabs()
        # self.displays("tab", "both")
    
    def displays(self, mode, pack_mode):
        self.root.geometry("640x480")
        notebook = ttk.Notebook(self.root)
        column_names = ("group", "name", "year")
        
        if mode == "tab":
            frame = Frame(notebook)
            notebook.add(frame, text="Data")
            treeview_data = ttk.Treeview(frame)
            treeview_data.configure(columns=column_names)
            treeview_data.heading("#0", text="ID")
            [treeview_data.heading(col, text=col.title()) for col in column_names]
            treeview_data.pack(fill=BOTH, expand=True)
        elif mode == "root":
            frame = Frame(self.root)
            
        if pack_mode == "both":
            notebook.pack(fill=BOTH, expand=True)
        elif pack_mode == 2:
            notebook.pack()
    
    def set_style(self, style_name) -> ttk.Style:
        self.style = ttk.Style()
        with open(style_name) as f:
            j = f.read()
            style_content = json.loads(j)
        
        # Styles
        ## Tabs
        # tab_config = {
        #     # "width": 25,
        #     # "padding": [0, 0],
        #     # "font": ("Calibri", 10, "bold")
        #     # "yscrollcommand": 
        # }
        # style_content["settings"]["TNotebook.Tab"]["configure"].update(tab_config)
        
        ## Table headings
        # table_headings_config = {
        #     # "anchor": "center",
        #     # "borderwidth": 5,
        #     # "relief": "groove"
        # }
        # style_content["settings"]["Treeview.Heading"]["configure"].update(table_headings_config)
        
        self.style.theme_create(**style_content)
        # style.theme_use(style_content["themename"])
    
    def set_root(self) -> None:
        self.root.title("Secret Santa")
        self.root.iconbitmap("santa.ico")
        self.root.minsize(640, 480)
        init_w = self.dim["w"] = 640
        init_h = self.dim["h"] = 480
        init_x = self.pos["x"] = int(
            (self.root.winfo_screenwidth() / 2) - (self.dim["w"] / 2))
        init_y = self.pos["y"] = int(
            (self.root.winfo_screenheight() / 2) - (self.dim["h"] / 2))
        self.root.geometry(
            self.upd_win(dim=(init_w, init_h), pos=(init_x, init_y))
            )
    
    def upd_win(self, dim: tuple, pos: tuple) -> str:
        geo_str = f'{dim[0]}x{dim[1]}+{pos[0]}+{pos[1]}'
        return geo_str
    
    def set_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.create_tab_run()
        self.create_tab_config()
        self.create_tab_pref()
        self.notebook.pack(fill=BOTH, expand=True)
    
    def create_tab_run(self):
        self.tab_run = ttk.Frame(self.notebook)
        # self.tab_run = ttk.Frame(self.notebook, style="TFrame", padding=10)
        self.notebook.add(self.tab_run, text="RUN")

        # btn_roll = ttk.Button(self.tab_run, text="Roll", command=self.run, style="Roll.TButton")
        # btn_roll.pack(fill="x", expand=True, pady=(0, 5))
        # btn_clear = ttk.Button(self.tab_run, text="Clear", command=self.clear, style="Clear.TButton")
        # btn_clear.pack(fill="x", expand=True, pady=(0, 5))

        self.table_run = ttk.Treeview(self.tab_run)
        self.table_run.configure(columns=("assigned"))
        self.table_run.heading("#0", text="Participant")
        # self.table_run = ttk.Treeview(self.tab_run, style="Treeview", height=255)
        # # self.table_run = ttk.Treeview(self.root, style="Treeview")
        # self.table_run.configure(columns=("assigned"))
        # # self.table_run.tag_configure("even_row", background="#B1D2A3")    
        # self.table_run.heading("#0", text="Participant", anchor=CENTER)
        # self.table_run.heading("assigned", text="Assigned", anchor=CENTER)

        # # self.table_run.column("#0", stretch=YES, minwidth=0, width=10)    
        # # self.table_run.column("assigned", stretch=NO, minwidth=10, width=10, anchor=CENTER)    
    
        # self.table_run.insert("", "end", text="1", values=("John", 30))
        # self.table_run.insert("", "end", text="2", values=("Alice", 25))
        # self.table_run.insert("", "end", text="3", values=("John", 20))
        # self.table_run.insert("", "end", text="4", values=("Alex", 19))
        # self.table_run.insert("", "end", text="5", values=("Erika", 27))
        # self.table_run.insert("", "end", text="6", values=("Matt", 38))
        # self.table_run.insert("", "end", text="7", values=("Natasha", 24))
        # self.table_run.insert("", "end", text="8", values=("Rudy", 22))
        # self.table_run.insert("", "end", text="9", values=("Helen", 32))
        # self.table_run.insert("", "end", text="10", values=("Gary", 34))
        # self.table_run.insert("", "end", text="11", values=("Mary", 21))
        # self.table_run.insert("", "end", text="12", values=("Jimmy", 40))
        # self.table_run.insert("", "end", text="13", values=("Tracy", 46))
        # self.table_run.insert("", "end", text="14", values=("Ben", 18))
        # self.table_run.insert("", "end", text="15", values=("Anne", 42))
        # self.table_run.insert("", "end", text="16", values=("Phil", 33))
        # self.table_run.insert("", "end", text="17", values=("Andrew", 26))
        # self.table_run.insert("", "end", text="18", values=("Christine", 28))
        # self.table_run.insert("", "end", text="19", values=("Amanda", 21))
        # self.table_run.insert("", "end", text="20", values=("Lucy", 31))

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
        self.root.bind("<Configure>", self.resize)
        self.root.mainloop()

    def resize(self, _) -> None:
        self.table_run.column("#0", width=self.root.winfo_width())
