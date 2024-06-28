import tkinter as tk
from tkinter import ttk


class Run:
    def __init__(self, ui):
        # Main
        self.ui = ui
        self.frame_main = None
        self.frame_act = None

        # Table
        self.table_main = None

        # Buttons
        self.btn_roll = None
        self.btn_clear = None

        # Columns to display in the table
        self.table_main_cols = ("member", "assigned")
        self.col_width = (self.ui.fixed_win["dim"][0] - 2 * (
                    self.ui.style_static["settings"]["TNotebook"]["configure"]["padding"][0] +
                    self.ui.style_static["settings"]["TFrame"]["configure"]["padding"][0])) // len(self.table_main_cols) - 3

        # Data
        self.table_main_data = {}

    def create_tab(self) -> None:
        """Creates the RUN tab"""

        # TFrame
        self.frame_main = ttk.Frame(
            self.ui.notebook,
            style="Run.TFrame"
        )
        self.frame_main.rowconfigure(0, weight=20)
        self.frame_main.rowconfigure(1, weight=80)
        self.frame_main.columnconfigure(0, weight=100)
        self.frame_main.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["tab_run"][0],
            pady=self.ui.grid_param["padding"]["tab_run"][1]
        )
        self.ui.notebook.add(
            self.frame_main
        )

        # Actions frame
        self.frame_act = ttk.Frame(
            self.frame_main,
            style="Act.Run.TFrame"
        )
        self.frame_act.rowconfigure(0, weight=50)
        self.frame_act.rowconfigure(1, weight=50)
        self.frame_act.columnconfigure(0, weight=100)
        self.frame_act.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["frame_run_act"][0],
            pady=self.ui.grid_param["padding"]["frame_run_act"][1]
        )

        ## Buttons
        self.btn_roll = ttk.Button(
            self.frame_act,
            command=self.action_roll,
            style="Roll.TButton",
            takefocus=False
        )
        self.btn_roll.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["btn_run_roll"][0],
            pady=self.ui.grid_param["padding"]["btn_run_roll"][1]
        )
        self.btn_clear = ttk.Button(
            self.frame_act,
            command=self.action_clear,
            style="Clear.TButton",
            takefocus=False
        )
        self.btn_clear.grid(
            row=1,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["btn_run_clear"][0],
            pady=self.ui.grid_param["padding"]["btn_run_clear"][1]
        )

        # Treeview
        self.table_main = ttk.Treeview(
            self.frame_main,
            style="TableRun.Treeview"
        )
        self.table_main.configure(columns=self.table_main_cols)
        self.table_main.grid(
            row=1,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["table_run"][0],
            pady=self.ui.grid_param["padding"]["table_run"][1]
        )

        ## Tags
        self.table_main.tag_configure(
            "oddrow",
            background="#C7DEB1"
        )
        self.update_tab()

    def update_tab(self) -> None:
        """Updates the RUN tab and its components"""

        self.ui.notebook.tab(self.frame_main, text=self.ui.disp_txt["run"])
        self.btn_roll.configure(text=self.ui.disp_txt["btn"]["roll"])
        self.btn_clear.configure(text=self.ui.disp_txt["btn"]["clear"])
        # self.table_main.configure(height=20)

        ## Headings & columns
        self.table_main.heading(
            "#0",
            text=""
        )
        self.table_main.column(
            "#0",
            stretch=tk.NO,
            minwidth=0,
            width=0
        )
        for i, v in enumerate(self.table_main_cols):
            self.table_main.heading(
                v,
                text=self.ui.disp_txt["tab_run_table_headings"][i],
                anchor=tk.CENTER
            )
            self.table_main.column(
                v,
                stretch=tk.YES,
                # minwidth=self.fixed_style["treeview.column"]["minwidth"],
                width=self.col_width,
                anchor=tk.CENTER
            )

        self.ui.empty_table(self.table_main)
        for i, (name, assigned) in enumerate(self.table_main_data.items()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            values = (f'{name.title()}', f'{", ".join([p.title() for p in assigned])}')
            self.table_main.insert("", "end", values=values, tags=tag)

    def action_roll(self) -> None:
        """Retrieves the randomized paired data"""

        if not self.ui.popup:
            self.table_main_data = self.ui.logic.run()
            self.update_tab()

    def action_clear(self) -> None:
        """Clears the retrieved data and the treeview"""

        if not self.ui.popup:
            self.table_main_data.clear()
            self.update_tab()