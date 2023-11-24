import os
import tkinter as tk
from tkinter import ttk


class Interface:
    def __init__(self, run_logic, upd_participants, participants=None, root_win=None):
        self.run_logic = run_logic
        self.update_participants = upd_participants
        self.participants = participants
        self.root = root_win
        # self.win_dim = {"w": 800, "h": 600}
        self.win_coords = {"x": 0, "y": 0}
        self.padding = 5
        self.ipadding = 20
        self.btn_width = 36

        self.notebook = None
        self.frame_run = None
        self.frame_config = None
        self.frame_test = None
        self.style = ttk.Style()
        self.style.theme_create(
            themename="santas",
            parent="alt",
            settings={
                "TNotebook": {
                    "configure": {
                        "borderwidth": 0,
                        "padding": self.padding,
                        "background": "#558B57"
                    }
                },
                "TNotebook.Tab": {
                    "configure": {
                        "width": 40,
                        "padding": [50, 10],
                        "font": ("Calibri", "12", "bold"),
                        "background": "#83AF7E",
                        "foreground": "#E0F7CB",
                        "anchor": "center"
                    },
                    "map": {
                        "background": [("selected", "#B1D2A3")],
                        "foreground": [("selected", "#276733")],
                        # "expand": [("selected", [1, 1, 1, 0])]
                    }
                },
                "TFrame": {
                    "configure": {
                        "background": "#B1D2A3",
                        "anchor": "center",
                    }
                },
                "TButton": {
                    "configure": {
                        "width": self.btn_width,
                        "font": ("Calibri", 32),
                        "foreground": "#E0F7CB",
                        "background": "#558B57",
                        "anchor": "center",
                    },
                    "map": {
                        "background": [("pressed", "#5EBC61"), ("active", "#4D9B50")]
                    }
                },
                "Treeview": {
                    "configure": {
                        "background": "#E0F7CB"
                    },
                },
                "Treeview.Heading": {
                    "configure": {
                        "background": "#83AF7E"
                    }
                }
            }
        )
        self.style.theme_use("santas")

        self.table_run = None
        self.table_config = None
        self.table_test = None

        self.results = {}
        self.res_labels = []

        self.set_root()
        self.generate_tabs()

    def set_root(self):
        self.root.title("Secret Santa")
        self.root.iconbitmap("santa.ico")
        # self.root.resizable(False, False)
        # self.win_coords["x"] = int((self.root.winfo_screenwidth() / 2) - (self.win_dim["w"] / 2))
        # self.win_coords["y"] = int((self.root.winfo_screenheight() / 2) - (self.win_dim["h"] / 2))

    def generate_tabs(self):
        self.notebook = ttk.Notebook(self.root)#, width=self.win_dim["w"], height=self.win_dim["h"])
        self.create_frame_run()
        self.create_frame_config()
        self.create_frame_test()
        self.notebook.grid(column=0, row=0, sticky="we")

    def create_frame_run(self):
        self.frame_run = ttk.Frame(self.notebook, style="TFrame", padding=self.ipadding)
        self.frame_run.grid(column=0, row=0, sticky="we")
        # self.frame_run.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.frame_run, text="Run")

        roll_btn = ttk.Button(self.frame_run, text="Roll", command=self.run, style="Roll.TButton")
        roll_btn.grid(column=0, row=0)
        clear_btn = ttk.Button(self.frame_run, text="Clear", command=self.clear_results, style="Clear.TButton")
        clear_btn.grid(column=0, row=1, pady=(20, 0))

        self.table_run = ttk.Treeview(self.frame_run, padding=5, height=18)
        self.table_run["columns"] = ("participant", "assigned")
        self.table_run.column("#0", width=0, stretch=tk.NO)
        self.table_run.tag_configure("even_row", background="#B1D2A3")
        self.table_run.heading("participant", text="Participant", anchor="center")
        self.table_run.heading("assigned", text="Assigned", anchor="center")
        self.table_run.grid(column=0, row=2, pady=(20, 0), sticky="nswe")

    def create_frame_config(self):
        self.frame_config = ttk.Frame(self.notebook, style="TFrame", padding=self.ipadding)
        self.frame_config.grid(column=0, row=0, sticky="we")
        self.notebook.add(self.frame_config, text="Configuration")

        self.table_config = ttk.Treeview(self.frame_config, padding=5, height=18)
        self.table_config["columns"] = ("family_id", "participant", "age", "except")
        self.table_config.column("#0", width=0, stretch=tk.NO)
        self.table_config.tag_configure("even_row", background="#B1D2A3")
        self.table_config.heading("family_id", text="Family ID", anchor="center")
        self.table_config.heading("participant", text="Participant", anchor="center")
        self.table_config.heading("age", text="Age", anchor="center")
        self.table_config.heading("except", text="Exceptions", anchor="center")
        self.table_config.grid(column=0, row=0, pady=(20, 0), sticky="nswe")

        upd_btn = ttk.Button(self.frame_config, text="Update", command=self.update_config, style="Update.TButton")
        upd_btn.grid(column=0, row=1, pady=(10, 0))
        open_config_btn = ttk.Button(self.frame_config, text="Open configuration file", command=self.open_config, style="OpenConfig.TButton")
        open_config_btn.grid(column=0, row=2, pady=(20, 0))

        self.update_config()

    def create_frame_test(self):
        self.frame_test = ttk.Frame(self.notebook, style="TFrame", padding=self.ipadding)
        self.frame_test.grid(column=0, row=0, sticky="we")
        self.notebook.add(self.frame_test, text="Test")

        self.table_test = ttk.Treeview(self.frame_test, padding=5, height=18)
        self.table_test["columns"] = ("family_id", "participant", "age", "except")
        self.table_test.column("#0", width=0, stretch=tk.NO)
        self.table_test.tag_configure("even_row", background="#B1D2A3")
        self.table_test.heading("family_id", text="Family ID", anchor="center")
        self.table_test.heading("participant", text="Participant", anchor="center")
        self.table_test.heading("age", text="Age", anchor="center")
        self.table_test.heading("except", text="Exceptions", anchor="center")
        self.table_test.grid(column=0, row=0, pady=(20, 0), sticky="nswe")

        upd_btn = ttk.Button(self.frame_test, text="Update", command=self.update_config, style="Update.TButton")
        upd_btn.grid(column=0, row=1, pady=(10, 0))
        open_config_btn = ttk.Button(self.frame_test, text="Open configuration file", command=self.open_config, style="OpenConfig.TButton")
        open_config_btn.grid(column=0, row=2, pady=(20, 0))

        self.update_test()

    def run(self):
        self.clear_results()
        self.results = self.run_logic()
        self.grid_results()

    def clear_results(self):
        self.results.clear()
        self.table_run.delete(*self.table_run.get_children())

    def grid_results(self):
        if self.results:
            row_num = 0
            for name, assigned in self.results.items():
                text = (f'{name.title()}', f'{", ".join([p.name for p in assigned])}')
                if row_num % 2 == 0:
                    self.table_run.insert(parent="", index=str(row_num), values=text, tags=("even_row"))
                else:
                    self.table_run.insert(parent="", index=str(row_num), values=text)
                # text = f'{name.title()}:\t\t{", ".join([p.name for p in assigned])}'
                # label = ttk.Label(self.table_run, text=text)
                # self.res_labels.append(label)
                # label.grid(column=0, row=row_num)
                row_num += 1

    def update_config(self):
        self.participants = self.update_participants()
        self.table_config.delete(*self.table_config.get_children())

        row_num = 0
        for p, member in self.participants.items():
            try:
                text = (f'{member.family_id}', f'{p}', f'{member.age}', f'{", ".join(m for m in member.exceptions)}')
                if row_num % 2 == 0:
                    self.table_config.insert(parent="", index=str(row_num), values=text, tags=("even_row"))
                else:
                    self.table_config.insert(parent="", index=str(row_num), values=text)
                row_num += 1
            except TypeError:
                pass

    def update_test(self):
        self.participants = self.update_participants()
        self.table_config.delete(*self.table_config.get_children())

        row_num = 0
        for p, member in self.participants.items():
            try:
                text = (f'{member.family_id}', f'{p}', f'{member.age}', f'{", ".join(m for m in member.exceptions)}')
                if row_num % 2 == 0:
                    self.table_config.insert(parent="", index=str(row_num), values=text, tags=("even_row"))
                else:
                    self.table_config.insert(parent="", index=str(row_num), values=text)
                row_num += 1
            except TypeError:
                pass

    @staticmethod
    def open_config():
        os.startfile("../config.json")