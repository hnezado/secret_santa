import json
from tkinter import *
from tkinter import ttk

palette = {
    1: "#558B57",
    2: "#83AF7E",
    3: "#E0F7CB",
    4: "#B1D2A3",
    5: "#276733",
    6: "#5EBC61",
    7: "#4D9B50"
}


class Interface:
    def __init__(self, style, logic) -> None:
        # Main window
        self.root = Tk()
        self.dim = {"w": 800, "h": 600}
        self.pos = {"x": 0, "y": 0}
        self.style = self.set_style(style_name=style)
        self.run = logic[0]
        self.clear = logic[1]
        
        # Components
        self.notebook = None
        self.tab_run = None
        self.tab_config = None
        self.tab_test = None
        
        self.set_root()
        self.set_tabs()
    
    def set_root(self) -> None:
        self.root.title("Secret Santa")
        self.root.iconbitmap("santa.ico")
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
    
    def set_style(self, style_name) -> ttk.Style:
        style = ttk.Style()
        with open(style_name) as f:
            j = f.read()
            style_content = json.loads(j)
        style.theme_create(**style_content)
        return style
    
    def set_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.create_tab_run()
        self.create_tab_config()
        self.create_tab_test()
        self.notebook.grid(column=0, row=0, sticky="we")
    
    def create_tab_run(self):
        self.tab_run = ttk.Frame(self.notebook, style="TFrame", padding=20)
        self.tab_run.grid(column=0, row=0, sticky="we")
        # # self.tab_run.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.tab_run, text="Run")

        btn_roll = ttk.Button(self.tab_run, text="Roll", command=self.run, style="Roll.TButton")
        btn_roll.grid(column=0, row=0)
        btn_clear = ttk.Button(self.tab_run, text="Clear", command=self.clear, style="Clear.TButton")
        btn_clear.grid(column=0, row=1, pady=(20, 0))

        # self.table_run = ttk.Treeview(self.tab_run, padding=5, height=18)
        # self.table_run["columns"] = ("participant", "assigned")
        # self.table_run.column("#0", width=0, stretch=NO)
        # self.table_run.tag_configure("even_row", background="#B1D2A3")
        # self.table_run.heading("participant", text="Participant", anchor="center")
        # self.table_run.heading("assigned", text="Assigned", anchor="center")
        # self.table_run.grid(column=0, row=2, pady=(20, 0), sticky="nswe")
    
    def create_tab_config(self):
        pass
    
    def create_tab_test(self):
        pass
    
    def display(self) -> None:
        self.root.mainloop()
