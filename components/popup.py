import tkinter as tk
import logging as log
from collections import OrderedDict


class Popup:
    def __init__(self, ui):
        # Main
        self.ui = ui
        self.popup = None

        # Base frames
        self.frame_data = None
        self.frame_actions = None
        self.frames_attrs = []

        # Data
        self.text_widgets = {}
        self.sel_member = None

    def create_base(self, mode):
        """Creates the popup base"""

        # Popup window
        self.action_close()
        self.popup = tk.Toplevel()
        self.popup.rowconfigure(0, weight=90)
        self.popup.rowconfigure(1, weight=10)
        self.popup.columnconfigure(0, weight=100)

        # Frames
        self.frame_data = tk.Frame(self.popup, padx=10, pady=10)
        if mode == "form":
            self.frame_data.columnconfigure(0, weight=25)
            self.frame_data.columnconfigure(1, weight=70)
            self.frame_data.columnconfigure(2, weight=5)
        elif mode == "info":
            self.frame_data.columnconfigure(0, weight=100)
        else:
            log.error("Invalid popup base mode")

        self.frame_data.grid(
            row=0,
            column=0,
            sticky=tk.NSEW
        )
        self.frame_actions = tk.Frame(self.popup, padx=10, pady=10,)
        self.frame_actions.rowconfigure(0, weight=100)
        self.frame_actions.columnconfigure(0, weight=50)
        self.frame_actions.columnconfigure(1, weight=50)
        self.frame_actions.grid(
            row=1,
            column=0,
            sticky=tk.NSEW
        )

    def generate_attribute_frame(self, attr_index: int, attr_name: str, is_list: bool) -> tk.Frame:
        """Returns a frame for one attribute"""

        attr_frame = tk.Frame(self.frame_data)
        attr_frame.grid(row=attr_index, column=0, sticky=tk.NSEW)
        if is_list:
            list_frame = tk.Frame(attr_frame)
            list_frame.grid(row=0, column=0, sticky=tk.NSEW)
            label = tk.Label(list_frame, text=f'{attr_name}: '.title(), width=10, height=1)
            text_box = tk.Text(list_frame, height=1)
            btn_add = tk.Button(list_frame, text="+", height=1, pady=-5, command=lambda ind=attr_index: self.action_add_row(ind))
            btn_add.grid(row=0, column=2, sticky=tk.NSEW)
        else:
            label = tk.Label(attr_frame, text=f'{attr_name}: '.title(), anchor="e", width=10, height=1)
            text_box = tk.Text(attr_frame, height=1)
        label.grid(row=0, column=0, sticky="NSW")
        text_box.grid(row=0, column=1, sticky=tk.NSEW)
        return attr_frame

    def open_add(self) -> None:
        """Opens a pop-up window allowing the data entry of a new member"""

        self.create_base(mode="form")

        for i, attr in enumerate(self.ui.logic.attrs):
            list_type = self.ui.logic.config[attr]["type"] == "list"
            frm = self.generate_attribute_frame(attr_index=i, attr_name=attr, is_list=list_type)
            self.frames_attrs.append(frm)

        # Action buttons
        btn_confirm = tk.Button(
            self.frame_actions,
            text="Confirm",
            height=1,
            padx=20,
            pady=10,
            command=self.action_confirm
        )
        btn_confirm.grid(
            row=1,
            column=0,
            sticky=tk.EW
        )
        btn_cancel = tk.Button(
            self.frame_actions,
            text="Cancel",
            height=1,
            padx=20,
            pady=10,
            command=self.action_close
        )
        btn_cancel.grid(
            row=1,
            column=1,
            sticky=tk.EW
        )

        self.popup.protocol("WM_DELETE_WINDOW", self.action_close)
        self.event_binding()
        self.set_geometry()

    def open_edit(self, member):
        """Opens a pop-up window allowing the selected member data edition"""
        # TODO Pendiente de añadir languages a los botones (y labels?)

        self.create_base(mode="form")
        self.sel_member = member


        row_index = 0
        for key, value in self.sel_member.items():
            if isinstance(value, list):
                if value:
                    label_key = tk.Label(self.frame_data, text=key.title())
                    label_key.grid(row=row_index, column=0, sticky="w")
                    text_box = tk.Text(self.frame_data, height=1, width=20)
                    text_box.insert(tk.END, value[0])
                    text_box.grid(row=row_index, column=1, sticky="nsew")
                    self.text_widgets[f"{key}#0"] = text_box
                    row_index += 1

                    for i, item in enumerate(value[1:], start=1):
                        label_key_empty = tk.Label(self.frame_data, text="")
                        label_key_empty.grid(row=row_index, column=0, sticky="w")
                        text_box = tk.Text(self.frame_data, height=1, width=20)
                        text_box.insert(tk.END, item)
                        text_box.grid(row=row_index, column=1, sticky="nsew")
                        self.text_widgets[f"{key}#{i}"] = text_box
                        row_index += 1
                else:
                    label_key = tk.Label(self.frame_data, text=key.title())
                    label_key.grid(row=row_index, column=0, sticky="w")
                    text_box = tk.Text(self.frame_data, height=1, width=20)
                    text_box.grid(row=row_index, column=1, sticky="nsew")
                    self.text_widgets[key] = text_box
                    row_index += 1
            else:
                label_key = tk.Label(self.frame_data, text=key.title())
                label_key.grid(row=row_index, column=0, sticky="w")
                text_box = tk.Text(self.frame_data, height=1, width=20)
                text_box.insert(tk.END, str(value))
                text_box.grid(row=row_index, column=1, sticky="nsew")
                self.text_widgets[key] = text_box
                row_index += 1

        button_frame = tk.Frame(self.popup)
        button_frame.grid(row=1, column=0, sticky="nsew")
        button_frame.columnconfigure(0, weight=50)
        button_frame.columnconfigure(1, weight=50)

        # Action buttons
        save_button = tk.Button(button_frame, text="Save", command=self.action_confirm)
        save_button.grid(row=0, column=0, sticky="e", padx=10, pady=10)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.action_close)
        cancel_button.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        self.popup.protocol("WM_DELETE_WINDOW", self.action_close)
        self.event_binding()
        self.set_geometry()

    def open_del(self, member) -> None:
        """Opens a pop-up window to allow deletion of the selected member"""

        self.create_base(mode="info")
        self.sel_member = member

        # Label
        label_confirm = tk.Label(
            self.frame_data,
            height=3,
            text=f'Do you want to delete the selected member: "{member.name}"?'
        )
        label_confirm.grid(
            row=0,
            column=1,
            sticky=tk.NSEW
        )

        # Buttons
        btn_confirm = tk.Button(
            self.frame_actions,
            text="Accept",
            command=self.action_pudel_confirm
        )
        btn_confirm.grid(
            row=0,
            column=0,
            sticky=tk.NSEW
        )
        btn_cancel = tk.Button(
            self.frame_actions,
            text="Cancel",
            command=self.action_close
        )
        btn_cancel.grid(
            row=0,
            column=1,
            sticky=tk.NSEW
        )

        self.popup.protocol("WM_DELETE_WINDOW", self.action_close)
        self.event_binding()
        self.set_geometry()

    def set_geometry(self) -> None:
        """Calculates the pop-up geometry centering it"""

        # Calculate popup window geometry
        self.popup.update()
        popup_w = self.popup.winfo_width()
        popup_h = self.popup.winfo_height()
        popup_x = self.ui.root.winfo_screenwidth() // 2 - (popup_w // 2)
        popup_y = self.ui.root.winfo_screenheight() // 4 - (popup_h // 2)
        self.popup.geometry(f'+{popup_x}+{popup_y}')

    def action_add_row(self, list_frame_index):
        """Adds a new row inside the attribute frame"""

        if isinstance(self.frames_attrs[list_frame_index], tk.Frame):
            sub_rows = self.frames_attrs[list_frame_index].winfo_children()
            if isinstance(sub_rows[0], tk.Frame):
                sub_row_index = len(sub_rows)
                print("ok:", sub_row_index)
                new_row_frame = tk.Frame(self.frames_attrs[list_frame_index])
                new_row_frame.grid(column=0, sticky=tk.NSEW)
                label = tk.Label(new_row_frame, text="", width=10, height=1)
                label.grid(row=0, column=0, sticky="NSW")
                text_box = tk.Text(new_row_frame, height=1)
                text_box.grid(row=0, column=1, sticky=tk.NSEW)
                btn_del = tk.Button(new_row_frame, text="-", command=lambda f=list_frame_index, r=sub_row_index: self.action_remove_row(attr_index=f, sub_row_index=r))
                btn_del.grid(row=0, column=2, sticky=tk.NSEW)
            else:
                log.warning(f'The first sub_row {sub_rows[0]} not a tk.Frame object')
        else:
            log.warning(f'The attribute {self.frames_attrs[list_frame_index]} is not a tk.Frame object')

        self.event_binding()
        self.popup.update()

    def action_remove_row(self, attr_index, sub_row_index):
        """Removes a specific sub_row inside the attribute frame"""

        parent_frame = self.frames_attrs[attr_index]
        sub_rows = parent_frame.winfo_children()

        if sub_row_index < len(sub_rows):
            sub_row = sub_rows[sub_row_index]
            sub_row.destroy()

            # Update the indices of remaining sub_rows
            remaining_sub_rows = parent_frame.winfo_children()
            for idx, row in enumerate(remaining_sub_rows):
                delete_button = row.grid_slaves(row=0, column=2)[0]
                if idx == 0:
                    delete_button.config(
                        command=lambda f=attr_index, r=idx: self.action_add_row(f)
                    )
                else:
                    delete_button.config(
                        command=lambda f=attr_index, r=idx: self.action_remove_row(attr_index=f, sub_row_index=r)
                    )
        else:
            log.warning("Invalid sub_row_index: %d", sub_row_index)

        self.event_binding()
        self.popup.update()

    def action_confirm(self) -> None:
        """Saves the new_data from the corresponding member"""

        test_member = OrderedDict([
            ("enabled", True),
            ("name", "ataulfo"),
            ("family_id", 99),
            ("age", "adult"),
            ("exceptions", ["PeterPan"]),
            ("person", False)
        ])

        self.ui.logic.add_member(test_member)


        # self.action_close()
        # self.ui.tab_conf.update_tab()

    def action_close(self):
        """Closes the popup"""

        self.sel_member = None

        if self.popup:
            self.popup.destroy()
            self.popup = None
        self.frames_attrs.clear()
        self.text_widgets.clear()
        self.ui.tab_conf.table_sel = {
            "row": None,
            "member": None
        }
        self.ui.update_tabs()

    def action_pudel_confirm(self) -> None:
        """Confirms the member deletion action"""

        self.ui.logic.del_member(self.ui.tab_conf.table_sel["member"])
        self.ui.tab_conf.select(None)
        self.action_close()

    def focus_prev_widget(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def event_binding(self):
        """Binds every hotkey to its component"""

        def bind_recursive(widget):
            """Recursively bind events to widgets"""
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    bind_recursive(child)
            else:
                widget.bind("<Tab>", self.focus_next_widget)
                widget.bind("<Shift-Tab>", self.focus_prev_widget)

        for frm in self.frames_attrs:
            bind_recursive(frm)
