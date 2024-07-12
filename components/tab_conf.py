import tkinter as tk
from tkinter import ttk
import Pmw
import os
import logging as log


class Configuration:
    def __init__(self, ui):
        # Main
        self.ui = ui
        self.frame_main = None
        self.frame_act = None
        self.table = None

        # Buttons
        self.btn_conf_open_data_file = None
        self.btn_conf_add = None
        self.btn_conf_edit = None
        self.btn_conf_del = None

        # Tips
        self.tip_add = None
        self.tip_edit = None
        self.tip_del = None

        # Table configuration
        self.table_cols = ("#0", "family_id", "member", "age", "exceptions")
        self.table_sel = {}
        self.first_col_width = 16 * 2 + self.ui.img["checked"].width()
        self.col_width = (self.ui.fixed_win["dim"][0] - 2 * (self.ui.style_static["settings"]["TNotebook"]["configure"]["padding"][0] + self.ui.style_static["settings"]["TFrame"]["configure"]["padding"][0]) - self.first_col_width) // (len(self.table_cols) - 1) - 3
        self.table_last_index = 0

        Pmw.initialise(self.ui.root)

    def create_tab(self) -> None:
        """Creates the CONFIGURATION tab"""

        # Frame
        self.frame_main = ttk.Frame(
            self.ui.notebook,
            style="Conf.TFrame"
        )
        self.frame_main.rowconfigure(0, weight=20)
        self.frame_main.rowconfigure(1, weight=80)
        self.frame_main.columnconfigure(0, weight=100)
        self.frame_main.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["tab_conf"][0],
            pady=self.ui.grid_param["padding"]["tab_conf"][1]
        )
        self.ui.notebook.add(
            self.frame_main
        )

        # Actions frame
        self.frame_act = ttk.Frame(
            self.frame_main,
            style="Act.Conf.TFrame"
        )
        self.frame_act.rowconfigure(0, weight=50)
        self.frame_act.rowconfigure(1, weight=50)
        self.frame_act.columnconfigure(0, weight=33)
        self.frame_act.columnconfigure(1, weight=33)
        self.frame_act.columnconfigure(2, weight=33)
        self.frame_act.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["frame_conf_act"][0],
            pady=self.ui.grid_param["padding"]["frame_conf_act"][1]
        )

        # Buttons
        self.btn_conf_open_data_file = ttk.Button(
            self.frame_act,
            command=self.action_open_config_file,
            style="OpenConfigFile.TButton",
            takefocus=False
        )
        self.btn_conf_open_data_file.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["btn_conf_open_config"][0],
            pady=self.ui.grid_param["padding"]["btn_conf_open_config"][1]
        )
        self.btn_conf_add = ttk.Button(
            self.frame_act,
            command=self.action_add,
            style="ActionConf.TButton",
            takefocus=False
        )
        self.btn_conf_add.grid(
            row=1,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["btn_conf_add"][0],
            pady=self.ui.grid_param["padding"]["btn_conf_add"][1]
        )
        self.btn_conf_edit = ttk.Button(
            self.frame_act,
            command=self.action_edit,
            style="ActionConf.TButton",
            takefocus=False
        )
        self.btn_conf_edit.grid(
            row=1,
            column=1,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["btn_conf_edit"][0],
            pady=self.ui.grid_param["padding"]["btn_conf_edit"][1]
        )
        self.btn_conf_del = ttk.Button(
            self.frame_act,
            command=self.action_del,
            style="ActionConf.TButton",
            takefocus=False
        )
        self.btn_conf_del.grid(
            row=1,
            column=2,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["btn_conf_del"][0],
            pady=self.ui.grid_param["padding"]["btn_conf_del"][1]
        )

        # Treeview
        self.table = ttk.Treeview(
            self.frame_main,
            style="TableConf.Treeview"
        )
        self.table.configure(columns=self.table_cols[1:])
        self.table.grid(
            row=1,
            column=0,
            sticky=tk.NSEW,
            padx=self.ui.grid_param["padding"]["table_conf"][0],
            pady=self.ui.grid_param["padding"]["table_conf"][1]
        )
        self.table_sel = {
            "row": None,
            "member": None
        }

        ## Tags
        self.table.tag_configure(
            "oddrow",
            background="#C7DEB1"
        )
        self.table.tag_configure(
            "select",
            background="#478ADD"
        )

        self.update_tab()

    def update_tab(self) -> None:
        """Updates the CONFIGURATION tab and its components"""

        self.ui.notebook.tab(self.frame_main, text=self.ui.disp_txt["conf"])
        self.btn_conf_open_data_file.configure(text=self.ui.disp_txt["btn"]["open_data"])
        self.btn_conf_add.configure(text="+")
        self.btn_conf_edit.configure(text="Y")
        self.btn_conf_del.configure(text="-")

        # Tooltips
        self.tip_add = Pmw.Balloon(self.ui.root)
        self.tip_add.bind(self.btn_conf_add, self.ui.disp_txt["btn"]["add_conf_table"])
        self.tip_edit = Pmw.Balloon(self.ui.root)
        self.tip_edit.bind(self.btn_conf_edit, self.ui.disp_txt["btn"]["edit_conf_table"])
        self.tip_del = Pmw.Balloon(self.ui.root)
        self.tip_del.bind(self.btn_conf_del, self.ui.disp_txt["btn"]["del_conf_table"])

        ## Headings & columns
        for i, v in enumerate(self.table_cols):
            if i == 0:
                self.table.heading(
                    v,
                    text=self.ui.disp_txt["tab_conf_table_headings"][i],
                    anchor=tk.CENTER
                )
                self.table.column(
                    v,
                    stretch=tk.NO,
                    minwidth=self.first_col_width,
                    width=self.first_col_width
                )
            else:
                self.table.heading(
                    v,
                    text=self.ui.disp_txt["tab_conf_table_headings"][i],
                    anchor=tk.CENTER
                )
                self.table.column(
                    v,
                    stretch=tk.YES,
                    width=self.col_width,
                    anchor=tk.CENTER
                )

        self.empty_table()
        self.ui.logic.load_members()
        self.ui.logic.parse_members()
        print(self.ui.logic.members)
        for i, member in enumerate(self.ui.logic.members):
            if self.table_sel["row"] == i:
                tags = "select"
            else:
                tags = ("evenrow" if i % 2 == 0 else "oddrow")
            img = self.ui.img["checked"] if member["enabled"] else self.ui.img["unchecked"]
            values = (f'{member["family_id"]}',
                      f'{member["name"].title()}',
                      f'{member["age"].title()}',
                      f'{", ".join([e.title() for e in member["exceptions"]])}')
            if "enabled" in tags:
                self.table.insert(
                    "",
                    "end",
                    id=self.table_last_index,
                    image=img,
                    values=values,
                    tags=tags
                )
            else:
                self.table.insert(
                    "",
                    "end",
                    id=self.table_last_index,
                    image=img,
                    values=values,
                    tags=tags
                )
            self.table_last_index += 1

    def action_open_config_file(self) -> None:
        """Opens the configuration file"""

        if not self.ui.pu.popup:
            os.system("notepad.exe " + self.ui.uset.user_settings["input_file"])

    def action_add(self) -> None:
        """Adds a new member to the config file"""

        if not self.ui.pu.popup:
            self.ui.pu.open_add()
            self.update_tab()

    def action_edit(self) -> None:
        """Edits an existing member from the config file"""

        if not self.ui.pu.popup:
            if self.table_sel["member"] is not None:
                self.ui.pu.open_edit(self.table_sel["member"])
                self.update_tab()

    def action_del(self) -> None:
        """Deletes an existing member from the config file"""

        if not self.ui.pu.popup:
            if self.table_sel["member"] is not None:
                self.ui.pu.open_del(self.table_sel["member"])
                self.update_tab()

    def action_swap_check(self, member_index: int) -> None:
        """Swaps the member status (enabled, disabled)"""

        self.ui.logic.members[member_index]["enabled"] = not self.ui.logic.members[member_index]["enabled"]

    def select(self, row, member=None):
        """Sets the current selection in the config treeview"""

        self.table_sel["row"] = row
        self.table_sel["member"] = member

    def empty_table(self) -> None:
        """Empties the config table and resets its index"""

        self.table.delete(*self.table.get_children())
        self.table_last_index = 0

    def on_click(self, event: tk.Event) -> str or None:
        """Called on click event"""

        if not self.ui.pu.popup:
            region = self.table.identify("region", event.x, event.y)
            if region == "separator":
                return self.ui.disable_resizing(event)
            elif region == "tree" or region == "cell":
                member = {}
                try:
                    row = int(self.table.identify_row(event.y))
                    col = int(self.table.identify_column(event.x)[1:])
                    try:
                        member = self.ui.logic.members[row]
                    except Exception:
                        log.error(f'The member with index "{row}" cannot be found')
                    if member:
                        if col == 0:
                            self.action_swap_check(member_index=row)
                            self.ui.logic.save_data()
                            self.update_tab()
                            pass
                        else:
                            if self.table_sel["row"] == row:
                                self.select(None)
                            else:
                                self.select(row, member)
                            self.update_tab()
                except Exception:
                    log.error("Cell coordinates cannot be calculated")

    def binds(self):
        """Sets the bindings for this tab"""

        self.table.bind("<Button-1>", self.on_click)
