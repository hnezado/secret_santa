import os
import json
import Pmw
import logging as log
from reportlab.graphics import renderPM
from tkinter import *
from tkinter import ttk
from user_settings import *
from tabs.run import Run
from tabs.configuration import Configuration
from tabs.preferences import Preferences


class Interface:
    def __init__(self, logic) -> None:
        # Main
        self.logic = logic
        self.uset = UserSettings()
        self.style = None

        # Style
        self.grid_param = self.get_grid_param()
        self.style_static = self.get_style_static()
        self.style_dynamic = self.get_style_dynamic()

        # Displayed text (language settings)
        self.lang = None
        self.disp_txt = None
        self.update_lang()

        # Windows
        self.root = Tk()
        self.fixed_win = {
            "minsize": (640, 480),
            "dim": (800, 600),
            "pos": (0, 0)
        }
        self.set_root()
        self.popup = None

        # Components
        self.notebook = ttk.Notebook(self.root)
        self.tab_run = Run(self)
        self.tab_conf = Configuration(self)
        self.tab_pref = Preferences(self)


        ## CONF
        self.tab_conf = None
        self.frame_conf_act = None
        self.btn_conf_open_data_file = None
        self.btn_conf_add = None
        self.btn_conf_edit = None
        self.btn_conf_del = None
        self.table_conf = None
        self.tip_add = None
        self.tip_edit = None
        self.tip_del = None

        ## Pop-ups
        self.puadd_frame_data = None
        self.puadd_frame_actions = None
        self.puedit_frame_data = None
        self.puedit_frame_actions = None
        self.pudel_frame_data = None
        self.pudel_frame_actions = None
        self.text_widgets = dict()
        
        # Row selected
        self.table_conf_sel = {
            "row": None,
            "member": None
        }
        
        # Columns to display in each table
        self.table_conf_cols = ("#0", "family_id", "member", "age", "exceptions")
        
        # Data
        self.img = {
            "add": PhotoImage(file="./images/add.png"),
            "edit": PhotoImage(file="./images/edit.png"),
            "del": PhotoImage(file="./images/del.png"),
            "checked": PhotoImage(file="./images/checked.png"),
            "unchecked": PhotoImage(file="./images/unchecked.png"),
            "en_flag": PhotoImage(file="./images/en.png"),
            "es_flag": PhotoImage(file="./images/es.png"),
            "fr_flag": PhotoImage(file="./images/fr.png"),
            "wip": PhotoImage(file="./images/wip.png")
        }

        # Columns & rows
        self.conf_first_col_width = 16 * 2 + self.img["checked"].width()
        self.conf_col_width = (self.fixed_win["dim"][0] - 2 * (self.style_static["settings"]["TNotebook"]["configure"]["padding"][0]+ + self.style_static["settings"]["TFrame"]["configure"]["padding"][0]) - self.conf_first_col_width) // (len(self.table_conf_cols) - 1) - 3
        self.table_conf_last_index = 0

        # Initialization
        Pmw.initialise(self.root)
        self.set_style()
        self.update_style()
        self.set_tabs()

    def update_lang(self, lang: str = None) -> None:
        """Updates the language data on the interface module"""

        def load_lang(language) -> dict:
            """Retrieves the selected language data"""
            with open("./user_settings/lang.json", encoding="utf-8") as f:
                raw = f.read()
                return json.loads(raw)[language]

        if lang:
            self.uset.update_lang(lang)
            self.uset.load_user_settings()
        self.lang = self.uset.get_lang()
        self.disp_txt = load_lang(self.lang)

    def set_root(self) -> None:
        """Generates the root window with its dimensions and position"""

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

        # Grid configuration
        self.root.rowconfigure(0, weight=100)
        self.root.columnconfigure(0, weight=100)

    @staticmethod
    def get_grid_param() -> dict:
        """Retrieves the static grid data"""
        
        with open("./user_settings/styles/static.json") as f:
            static = f.read()
            return json.loads(static)["grid"]

    @staticmethod
    def get_style_static() -> dict:
        """Retrieves the static style data"""
        
        with open("./user_settings/styles/static.json") as f:
            static = f.read()
            return json.loads(static)["style"]

    def get_style_dynamic(self) -> dict:
        """Retrieves the dynamic style data"""
        
        with open(self.uset.user_settings["style"]) as f:
            dynamic = f.read()
            return json.loads(dynamic)

    def set_style(self) -> None:
        """Attempts to create a new style and applies it to the interface"""
        
        # Style creation
        self.style = ttk.Style()
        try:
            self.style.theme_create(**self.style_static)
        except:
            log.info(f'Theme {self.style_static["themename"]} already exists')
        
        # Style application
        self.style.theme_use(self.style_static["themename"])

    def update_style(self) -> None:
        """Updates the static style data with the dynamic style data"""
        
        for component, modes in self.style_dynamic.items():
            for mode in modes:
                if mode == "configure":
                    self.style.configure(
                        component,
                        **modes[mode]
                    )
                elif mode == "map":
                    self.style.map(
                        component,
                        **modes[mode]
                    )
                else:
                    log.info(f'Ignoring style mode {mode}')

    def set_tabs(self) -> None:
        """Set the notebook and its tabs"""
        
        self.tab_run.create_tab()
        # self.create_tab_conf()
        self.tab_pref.create_tab()
        self.notebook.grid(
            row=0,
            column=0,
            sticky=NSEW
        )

    def create_tab_conf(self) -> None:
        """Creates the CONFIGURATION tab"""
        
        # Frame
        self.tab_conf = ttk.Frame(
            self.notebook,
            style="Conf.TFrame"
        )
        self.tab_conf.rowconfigure(0, weight=20)
        self.tab_conf.rowconfigure(1, weight=80)
        self.tab_conf.columnconfigure(0, weight=100)
        self.tab_conf.grid(
            row=0,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["tab_conf"][0],
            pady=self.grid_param["padding"]["tab_conf"][1]
        )
        self.notebook.add(
            self.tab_conf
        )
        
        # Actions frame
        self.frame_conf_act = ttk.Frame(
            self.tab_conf,
            style="Act.Conf.TFrame"
        )
        self.frame_conf_act.rowconfigure(0, weight=50)
        self.frame_conf_act.rowconfigure(1, weight=50)
        self.frame_conf_act.columnconfigure(0, weight=33)
        self.frame_conf_act.columnconfigure(1, weight=33)
        self.frame_conf_act.columnconfigure(2, weight=33)
        self.frame_conf_act.grid(
            row=0,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["frame_conf_act"][0],
            pady=self.grid_param["padding"]["frame_conf_act"][1]
        )

        # Buttons
        self.btn_conf_open_data_file = ttk.Button(
            self.frame_conf_act,
            command=self.action_open_config_file,
            style="OpenConfigFile.TButton",
            takefocus=False
        )
        self.btn_conf_open_data_file.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_conf_open_config"][0],
            pady=self.grid_param["padding"]["btn_conf_open_config"][1]
        )
        self.btn_conf_add = ttk.Button(
            self.frame_conf_act,
            command=self.action_add,
            style="ActionConf.TButton",
            takefocus=False
        )
        self.btn_conf_add.grid(
            row=1,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_conf_add"][0],
            pady=self.grid_param["padding"]["btn_conf_add"][1]
        )
        self.btn_conf_edit = ttk.Button(
            self.frame_conf_act,
            command=self.action_edit,
            style="ActionConf.TButton",
            takefocus=False
        )
        self.btn_conf_edit.grid(
            row=1,
            column=1,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_conf_edit"][0],
            pady=self.grid_param["padding"]["btn_conf_edit"][1]
        )
        self.btn_conf_del = ttk.Button(
            self.frame_conf_act,
            command=self.action_del,
            style="ActionConf.TButton",
            takefocus=False
        )
        self.btn_conf_del.grid(
            row=1,
            column=2,
            sticky=NSEW,
            padx=self.grid_param["padding"]["btn_conf_del"][0],
            pady=self.grid_param["padding"]["btn_conf_del"][1]
        )

        # Treeview
        self.table_conf = ttk.Treeview(
            self.tab_conf,
            style="TableConf.Treeview"
        )
        self.table_conf.configure(columns=self.table_conf_cols[1:])
        self.table_conf.grid(
            row=1,
            column=0,
            sticky=NSEW,
            padx=self.grid_param["padding"]["table_conf"][0],
            pady=self.grid_param["padding"]["table_conf"][1]
        )
        
        ## Tags
        self.table_conf.tag_configure(
            "oddrow",
            background="#C7DEB1"
        )
        self.table_conf.tag_configure(
            "select",
            background="#478ADD"
        )

        self.update_tab_conf()

    def update_tab_conf(self) -> None:
        """Updates the CONFIGURATION tab and its components"""
        
        self.notebook.tab(self.tab_conf, text=self.disp_txt["conf"])
        self.btn_conf_open_data_file.configure(text=self.disp_txt["btn"]["open_data"])
        self.btn_conf_add.configure(text="+")
        self.btn_conf_edit.configure(text="Y")
        self.btn_conf_del.configure(text="-")
        
        # Tooltips
        self.tip_add = Pmw.Balloon(self.root)
        self.tip_add.bind(self.btn_conf_add, self.disp_txt["btn"]["add_conf_table"])
        self.tip_edit = Pmw.Balloon(self.root)
        self.tip_edit.bind(self.btn_conf_edit, self.disp_txt["btn"]["edit_conf_table"])
        self.tip_del = Pmw.Balloon(self.root)
        self.tip_del.bind(self.btn_conf_del, self.disp_txt["btn"]["del_conf_table"])
        
        ## Headings & columns
        for i, v in enumerate(self.table_conf_cols):
            if i == 0:
                self.table_conf.heading(
                    v,
                    text=self.disp_txt["tab_conf_table_headings"][i],
                    anchor=CENTER
                )
                self.table_conf.column(
                    v,
                    stretch=NO,
                    minwidth=self.conf_first_col_width,
                    width=self.conf_first_col_width
                )
            else:
                self.table_conf.heading(
                    v,
                    text=self.disp_txt["tab_conf_table_headings"][i],
                    anchor=CENTER
                )
                self.table_conf.column(
                    v,
                    stretch=YES,
                    width=self.conf_col_width,
                    anchor=CENTER
                )
        
        self.empty_table(self.table_conf)
        self.logic.read_members()
        self.logic.parse_members()
        for i, member in enumerate(self.logic.members.values()):
            if self.table_conf_sel["row"] == i:
                tags = "select"
            else:
                tags = ("evenrow" if i % 2 == 0 else "oddrow")
            img = self.img["checked"] if member.enabled else self.img["unchecked"]
            values = (f'{member.family_id}',
                      f'{member.name.title()}',
                      f'{member.age.title()}',
                      f'{", ".join([e.title() for e in member.exceptions])}')
            if "enabled" in tags:
                self.table_conf.insert(
                    "",
                    "end",
                    id=self.table_conf_last_index,
                    image=img,
                    values=values,
                    tags=tags
                )
            else:
                self.table_conf.insert(
                    "", 
                    "end",
                    id=self.table_conf_last_index,
                    image=img,
                    values=values,
                    tags=tags
                )
            self.table_conf_last_index += 1

    def empty_table(self, table: ttk.Treeview) -> None:
        """Empties the config table and resets its index"""
        
        table.delete(*table.get_children())
        self.table_conf_last_index = 0

    def update_tabs(self):
        """Updates every tab"""

        self.tab_run.update_tab()
        # self.tab_conf.update_tab()
        self.tab_pref.update_tab()

    def action_open_config_file(self) -> None:
        """Opens the configuration file"""
        
        if not self.popup:
            os.system("notepad.exe " + self.uset.user_settings["input_file"])

    def action_swap_check(self, member: object) -> None:
        """Swaps the member status (enabled, disabled)"""

        self.logic.members[member.name.lower()].enabled = not self.logic.members[member.name.lower()].enabled

    def action_save(self, member: object) -> None:
        """Saves the new_data from the corresponding member"""

        for key, widget in self.text_widgets.items():
            if '#' in key:
                main_key, index = key.rsplit('#', 1)
                index = int(index)
                if main_key not in vars(member):
                    setattr(member, main_key, [])
                while len(getattr(member, main_key)) <= index:
                    getattr(member, main_key).append("")
                value = widget.get("1.0", END).strip()
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                getattr(member, main_key)[index] = value
            else:
                value = widget.get("1.0", END).strip()
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                setattr(member, key, value)

        for key, value in vars(member).items():
            if isinstance(value, list):
                cleaned_list = [item for item in value if item]
                setattr(member, key, cleaned_list)

            # Actualiza el miembro en la lista
        for i, m in enumerate(self.logic.members):
            if m["name"] == member.name:
                self.logic.members[i] = member
                break

        self.logic.update_member(member)
        self.popup_close()
        self.update_tab_conf()

    def action_add(self) -> None:
        """Adds a new member to the config file"""
        
        if not self.popup:
            self.popup_open_add()
            self.update_tab_conf()
    
    def action_edit(self) -> None:
        """Edits an existing member from the config file"""
        
        if not self.popup:
            if self.table_conf_sel["member"] is not None:
                self.popup_open_edit(self.table_conf_sel["member"])
                self.update_tab_conf()

    def action_del(self) -> None:
        """Deletes an existing member from the config file"""
        
        if not self.popup:
            if self.table_conf_sel["member"] is not None:
                self.popup_open_del(self.table_conf_sel["member"])
                self.update_tab_conf()
    
    def action_puadd_confirm(self) -> None:
        """Confirms (inserts) the adding member action"""
        
        print(f'Adding new member data!')
    
    def action_puedit_confirm(self, member) -> None:
        """Confirms (overrides) the editing member data action"""

        print(f'Overriding member data from: {self.table_conf_sel["member"]}!')

    def action_pudel_confirm(self) -> None:
        """Confirms the member deletion action"""
        
        self.logic.del_member(self.table_conf_sel["member"])
        self.remove_conf_sel()
        self.popup_close()
        self.update_tab_conf()

    def popup_open_add(self) -> None:
        """Opens a pop-up window allowing the data entry of a new member"""

        # Popup window
        try:
            self.popup_close()
        except:
            pass
        self.popup = Toplevel()
        self.popup.rowconfigure(0, weight=90)
        self.popup.rowconfigure(1, weight=10)
        self.popup.columnconfigure(0, weight=100)
        
        # Frames
        self.puadd_frame_data = Frame(self.popup)
        # [frame_data.rowconfigure(i, weight=100//len(member_attrs)) for i in range(len(member_attrs))]
        self.puadd_frame_data.columnconfigure(0, weight=30)
        self.puadd_frame_data.columnconfigure(1, weight=70)
        self.puadd_frame_data.grid(
            row=0,
            column=0,
            sticky=NSEW
        )
        self.puadd_frame_actions = Frame(self.popup)
        self.puadd_frame_actions.rowconfigure(0, weight=100)
        self.puadd_frame_actions.columnconfigure(0, weight=50)
        self.puadd_frame_actions.columnconfigure(1, weight=50)
        self.puadd_frame_actions.grid(
            row=1,
            column=0,
            sticky=NSEW
        )
        
        # Buttons
        btn_confirm = Button(
            self.puadd_frame_actions,
            text="Confirm",
            command=self.action_puadd_confirm
        )
        btn_confirm.grid(
            row=1,
            column=0,
            sticky=NSEW
        )
        btn_cancel = Button(
            self.puadd_frame_actions,
            text="Cancel",
            command=self.popup_close
        )
        btn_cancel.grid(
            row=1,
            column=1,
            sticky=NSEW
        )

        self.popup.protocol("WM_DELETE_WINDOW", self.popup_close)
        self.popup_upd_add()

    def popup_upd_add(self) -> None:
        """Updates the new member data addition pop-up"""
        
        for i, param in enumerate(self.logic.member_attrs):
            label = Label(self.puadd_frame_data, height=1, text=f'{param}: '.title())
            label.grid(row=i, column=0, sticky="NSW")
            text_box = Text(self.puadd_frame_data, height=1)
            text_box.grid(row=i, column=1, sticky=NSEW)

        self.popup_set_geometry(self.popup)

    def popup_open_edit(self, member):
        """Opens a pop-up window allowing the selected member data edition"""
        # TODO Pendiente de añadir languages a los botones (y labels?)

        # Clear widgets
        try:
            for widget in self.puadd_frame_data.winfo_children():
                widget.destroy()
        except:
            pass

        member_attrs = vars(member)

        # Popup window
        try:
            self.popup_close()
        except:
            pass
        self.popup = Toplevel()
        self.popup.rowconfigure(0, weight=90)
        self.popup.rowconfigure(1, weight=10)
        self.popup.columnconfigure(0, weight=100)

        table_frame = Frame(self.popup)
        table_frame.grid(row=0, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=25, minsize=100)
        table_frame.columnconfigure(1, weight=75)

        row_index = 0
        for key, value in member_attrs.items():
            if isinstance(value, list):
                if value:
                    label_key = Label(table_frame, text=key.title())
                    label_key.grid(row=row_index, column=0, sticky="w")
                    text_box = Text(table_frame, height=1, width=20)
                    text_box.insert(END, value[0])
                    text_box.grid(row=row_index, column=1, sticky="nsew")
                    self.text_widgets[f"{key}#0"] = text_box
                    row_index += 1

                    for i, item in enumerate(value[1:], start=1):
                        label_key_empty = Label(table_frame, text="")
                        label_key_empty.grid(row=row_index, column=0, sticky="w")
                        text_box = Text(table_frame, height=1, width=20)
                        text_box.insert(END, item)
                        text_box.grid(row=row_index, column=1, sticky="nsew")
                        self.text_widgets[f"{key}#{i}"] = text_box
                        row_index += 1
                else:
                    label_key = Label(table_frame, text=key.title())
                    label_key.grid(row=row_index, column=0, sticky="w")
                    text_box = Text(table_frame, height=1, width=20)
                    text_box.grid(row=row_index, column=1, sticky="nsew")
                    self.text_widgets[key] = text_box
                    row_index += 1
            else:
                label_key = Label(table_frame, text=key.title())
                label_key.grid(row=row_index, column=0, sticky="w")
                text_box = Text(table_frame, height=1, width=20)
                text_box.insert(END, str(value))
                text_box.grid(row=row_index, column=1, sticky="nsew")
                self.text_widgets[key] = text_box
                row_index += 1

        # Crear un frame para los botones
        button_frame = Frame(self.popup)
        button_frame.grid(row=1, column=0, sticky="nsew")
        button_frame.columnconfigure(0, weight=50)
        button_frame.columnconfigure(1, weight=50)

        # Agregar los botones de Save y Cancel
        save_button = Button(button_frame, text="Save", command=lambda m=member: self.action_save(m))
        save_button.grid(row=0, column=0, sticky="e", padx=10, pady=10)

        cancel_button = Button(button_frame, text="Cancel", command=self.popup_close)
        cancel_button.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        self.popup.protocol("WM_DELETE_WINDOW", self.popup_close)
        self.popup_upd_edit()

    # TODO pendiente update edit pop-up
    def popup_upd_edit(self) -> None:
        """Updates the member data edition pop-up"""

        self.popup_set_geometry(self.popup)

    def popup_open_del(self, member) -> None:
        """Opens a pop-up window to allow deletion of the selected member"""

        # Popup window
        try:
            self.popup_close()
        except:
            pass
        self.popup = Toplevel()
        self.popup.rowconfigure(0, weight=50)
        self.popup.rowconfigure(1, weight=50)
        self.popup.columnconfigure(0, weight=100)

        # Frames
        self.pudel_frame_data = Frame(self.popup)
        self.pudel_frame_data.rowconfigure(0, weight=100)
        self.pudel_frame_data.columnconfigure(0, weight=100)
        self.pudel_frame_data.grid(
            row=0,
            column=0,
            sticky=NSEW
        )
        self.pudel_frame_actions = Frame(self.popup)
        self.pudel_frame_actions.rowconfigure(0, weight=100)
        self.pudel_frame_actions.columnconfigure(0, weight=50)
        self.pudel_frame_actions.columnconfigure(1, weight=50)
        self.pudel_frame_actions.grid(
            row=1,
            column=0,
            sticky=NSEW
        )
        
        # Label
        label_confirm = Label(
            self.pudel_frame_data,
            height=3,
            text=f'Do you want to delete the selected member: "{member.name}"?'
        )
        label_confirm.grid(
            row=0,
            column=1,
            sticky=NSEW
        )
        
        # Buttons
        btn_confirm = Button(
            self.pudel_frame_actions,
            text="Accept",
            command=self.action_pudel_confirm
        )
        btn_confirm.grid(
            row=0,
            column=0,
            sticky=NSEW
        )
        btn_cancel = Button(
            self.pudel_frame_actions,
            text="Cancel",
            command=self.popup_close
        )
        btn_cancel.grid(
            row=0,
            column=1,
            sticky=NSEW
        )
        
        self.popup.protocol("WM_DELETE_WINDOW", self.popup_close)
        self.popup_upd_del()
        
    # TODO pendiente update del pop-up
    def popup_upd_del(self) -> None:
        """Updates the member data deletion pop-up"""
        
        self.popup_set_geometry(self.popup)
        
    def popup_set_geometry(self, popup) -> None:
        """Calculates the pop-up geometry centering it"""
        
        # Calculate popup window geometry
        popup.update()
        popup_w = popup.winfo_width()
        popup_h = popup.winfo_height()
        popup_x = self.root.winfo_screenwidth() // 2 - (popup_w // 2)
        popup_y = self.root.winfo_screenheight() // 2 - (popup_h // 2)
        popup.geometry(f'{popup_w}x{popup_h}+{popup_x}+{popup_y}')

    def popup_close(self) -> None:
        """Closes the popup and sets some variables"""

        if self.popup:
            self.popup.destroy()
            self.popup = None
        self.text_widgets.clear()
        self.table_conf_sel = self.table_conf_sel = {
            "row": None,
            "member": None
        }
        self.update_tab_run()
        self.update_tab_conf()
        self.update_tab_pref()

    @staticmethod
    def disable_resizing(_) -> str:
        """Disables the column resizing"""
        
        return "break"

    def on_click_config(self, event: Event) -> str | None:
        """Called on click event"""
        
        if not self.popup:
            region = self.table_conf.identify("region", event.x, event.y)
            if region == "separator":
                return self.disable_resizing(event)
            elif region == "tree" or region == "cell":
                try:
                    row = int(self.table_conf.identify_row(event.y))
                    col = int(self.table_conf.identify_column(event.x)[1:])
                    try:
                        member = list(self.logic.members.values())[row]
                    except Exception:
                        log.error(f'The member with index "{row}" cannot be found')
                    if col == 0:
                        self.action_swap_check(member)
                        self.logic.save_data()
                        self.update_tab_conf()
                    else:
                        if self.table_conf_sel["row"] == row:
                            self.remove_conf_sel()
                        else:
                            self.table_conf_sel["row"] = row
                            self.table_conf_sel["member"] = member
                        self.update_tab_conf()
                except Exception:
                    log.error("Cell coordinates cannot be calculated")

    def remove_conf_sel(self) -> None:
        """Removes the current selection in the config treeview"""
    
        self.table_conf_sel["row"] = None
        self.table_conf_sel["member"] = None

    def display(self) -> None:
        """Main interface"""
        
        self.tab_run.table_main.bind("<Button-1>", self.disable_resizing)
        # self.tab_conf.table_conf.bind("<Button-1>", self.on_click_config)
        self.root.mainloop()
