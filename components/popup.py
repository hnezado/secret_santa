import tkinter as tk
import logging as log


class Popup:
    def __init__(self, ui):
        # Main
        self.ui = ui
        self.popup = None

        self.puadd_frame_data = None
        self.puadd_frame_actions = None
        self.puedit_frame_data = None
        self.puedit_frame_actions = None
        self.pudel_frame_data = None
        self.pudel_frame_actions = None
        self.text_widgets = dict()

        self.sel_member = None

    def open_add(self) -> None:
        """Opens a pop-up window allowing the data entry of a new member"""

        # Popup window
        self.action_close()
        self.popup = tk.Toplevel()
        self.popup.rowconfigure(0, weight=90)
        self.popup.rowconfigure(1, weight=10)
        self.popup.columnconfigure(0, weight=100)

        # Frames
        self.puadd_frame_data = tk.Frame(self.popup)
        # [frame_data.rowconfigure(i, weight=100//len(member_attrs)) for i in range(len(member_attrs))]
        self.puadd_frame_data.columnconfigure(0, weight=30)
        self.puadd_frame_data.columnconfigure(1, weight=70)
        self.puadd_frame_data.grid(
            row=0,
            column=0,
            sticky=tk.NSEW
        )
        self.puadd_frame_actions = tk.Frame(self.popup)
        self.puadd_frame_actions.rowconfigure(0, weight=100)
        self.puadd_frame_actions.columnconfigure(0, weight=50)
        self.puadd_frame_actions.columnconfigure(1, weight=50)
        self.puadd_frame_actions.grid(
            row=1,
            column=0,
            sticky=tk.NSEW
        )

        # Buttons
        btn_confirm = tk.Button(
            self.puadd_frame_actions,
            text="Confirm",
            command=self.action_confirm
        )
        btn_confirm.grid(
            row=1,
            column=0,
            sticky=tk.NSEW
        )
        btn_cancel = tk.Button(
            self.puadd_frame_actions,
            text="Cancel",
            command=self.action_close
        )
        btn_cancel.grid(
            row=1,
            column=1,
            sticky=tk.NSEW
        )

        self.popup.protocol("WM_DELETE_WINDOW", self.action_close)
        self.upd_add()

    def upd_add(self) -> None:
        """Updates the new member data addition pop-up"""

        for i, param in enumerate(self.ui.logic.member_attrs):
            label = tk.Label(self.puadd_frame_data, height=1, text=f'{param}: '.title())
            label.grid(row=i, column=0, sticky="NSW")
            text_box = tk.Text(self.puadd_frame_data, height=1)
            text_box.grid(row=i, column=1, sticky=tk.NSEW)

        self.set_geometry()

    def open_edit(self, member):
        """Opens a pop-up window allowing the selected member data edition"""
        # TODO Pendiente de añadir languages a los botones (y labels?)

        self.sel_member = member

        # Clear widgets
        try:
            for widget in self.puadd_frame_data.winfo_children():
                widget.destroy()
        except Exception:
            log.error("Error cleaning popup widgets")

        # Popup window
        self.action_close()
        self.popup = tk.Toplevel()
        self.popup.rowconfigure(0, weight=90)
        self.popup.rowconfigure(1, weight=10)
        self.popup.columnconfigure(0, weight=100)

        table_frame = tk.Frame(self.popup)
        table_frame.grid(row=0, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=25, minsize=100)
        table_frame.columnconfigure(1, weight=75)

        row_index = 0
        for key, value in member.items():
            if isinstance(value, list):
                if value:
                    label_key = tk.Label(table_frame, text=key.title())
                    label_key.grid(row=row_index, column=0, sticky="w")
                    text_box = tk.Text(table_frame, height=1, width=20)
                    text_box.insert(tk.END, value[0])
                    text_box.grid(row=row_index, column=1, sticky="nsew")
                    self.text_widgets[f"{key}#0"] = text_box
                    row_index += 1

                    for i, item in enumerate(value[1:], start=1):
                        label_key_empty = tk.Label(table_frame, text="")
                        label_key_empty.grid(row=row_index, column=0, sticky="w")
                        text_box = tk.Text(table_frame, height=1, width=20)
                        text_box.insert(tk.END, item)
                        text_box.grid(row=row_index, column=1, sticky="nsew")
                        self.text_widgets[f"{key}#{i}"] = text_box
                        row_index += 1
                else:
                    label_key = tk.Label(table_frame, text=key.title())
                    label_key.grid(row=row_index, column=0, sticky="w")
                    text_box = tk.Text(table_frame, height=1, width=20)
                    text_box.grid(row=row_index, column=1, sticky="nsew")
                    self.text_widgets[key] = text_box
                    row_index += 1
            else:
                label_key = tk.Label(table_frame, text=key.title())
                label_key.grid(row=row_index, column=0, sticky="w")
                text_box = tk.Text(table_frame, height=1, width=20)
                text_box.insert(tk.END, str(value))
                text_box.grid(row=row_index, column=1, sticky="nsew")
                self.text_widgets[key] = text_box
                row_index += 1

        # Crear un frame para los botones
        button_frame = tk.Frame(self.popup)
        button_frame.grid(row=1, column=0, sticky="nsew")
        button_frame.columnconfigure(0, weight=50)
        button_frame.columnconfigure(1, weight=50)

        # Agregar los botones de Save y Cancel
        save_button = tk.Button(button_frame, text="Save", command=self.action_confirm)
        save_button.grid(row=0, column=0, sticky="e", padx=10, pady=10)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.action_close)
        cancel_button.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        self.popup.protocol("WM_DELETE_WINDOW", self.action_close)
        self.upd_edit()

    # TODO pendiente update edit pop-up
    def upd_edit(self) -> None:
        """Updates the member data edition pop-up"""

        self.set_geometry()

    def open_del(self, member) -> None:
        """Opens a pop-up window to allow deletion of the selected member"""

        self.sel_member = member

        # Popup window
        self.action_close()
        self.popup = tk.Toplevel()
        self.popup.rowconfigure(0, weight=50)
        self.popup.rowconfigure(1, weight=50)
        self.popup.columnconfigure(0, weight=100)

        # Frames
        self.pudel_frame_data = tk.Frame(self.popup)
        self.pudel_frame_data.rowconfigure(0, weight=100)
        self.pudel_frame_data.columnconfigure(0, weight=100)
        self.pudel_frame_data.grid(
            row=0,
            column=0,
            sticky=tk.NSEW
        )
        self.pudel_frame_actions = tk.Frame(self.popup)
        self.pudel_frame_actions.rowconfigure(0, weight=100)
        self.pudel_frame_actions.columnconfigure(0, weight=50)
        self.pudel_frame_actions.columnconfigure(1, weight=50)
        self.pudel_frame_actions.grid(
            row=1,
            column=0,
            sticky=tk.NSEW
        )

        # Label
        label_confirm = tk.Label(
            self.pudel_frame_data,
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
            self.pudel_frame_actions,
            text="Accept",
            command=self.action_pudel_confirm
        )
        btn_confirm.grid(
            row=0,
            column=0,
            sticky=tk.NSEW
        )
        btn_cancel = tk.Button(
            self.pudel_frame_actions,
            text="Cancel",
            command=self.action_close
        )
        btn_cancel.grid(
            row=0,
            column=1,
            sticky=tk.NSEW
        )

        self.popup.protocol("WM_DELETE_WINDOW", self.action_close)
        self.upd_del()

    # TODO pendiente update del pop-up
    def upd_del(self) -> None:
        """Updates the member data deletion pop-up"""

        self.set_geometry()

    def set_geometry(self) -> None:
        """Calculates the pop-up geometry centering it"""

        # Calculate popup window geometry
        self.popup.update()
        popup_w = self.popup.winfo_width()
        popup_h = self.popup.winfo_height()
        popup_x = self.ui.root.winfo_screenwidth() // 2 - (popup_w // 2)
        popup_y = self.ui.root.winfo_screenheight() // 2 - (popup_h // 2)
        self.popup.geometry(f'{popup_w}x{popup_h}+{popup_x}+{popup_y}')

    def action_confirm(self) -> None:
        """Saves the new_data from the corresponding member"""

        for key, widget in self.text_widgets.items():
            if '#' in key:
                main_key, index = key.rsplit('#', 1)
                index = int(index)
                if main_key not in vars(self.sel_member):
                    setattr(self.sel_member, main_key, [])
                while len(getattr(self.sel_member, main_key)) <= index:
                    getattr(self.sel_member, main_key).append("")
                value = widget.get("1.0", tk.END).strip()
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                getattr(self.sel_member, main_key)[index] = value
            else:
                value = widget.get("1.0", tk.END).strip()
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                setattr(self.sel_member, key, value)

        for key, value in vars(self.sel_member).items():
            if isinstance(value, list):
                cleaned_list = [item for item in value if item]
                setattr(self.sel_member, key, cleaned_list)

            # Actualiza el miembro en la lista
        for i, m in enumerate(self.ui.logic.members):
            if m["name"] == self.sel_member.name:
                self.ui.logic.members[i] = self.sel_member
                break

        self.ui.logic.update_member(self.sel_member)
        self.action_close()
        self.ui.tab_conf.update_tab()

    def action_close(self):
        """Closes the popup"""

        self.sel_member = None

        if self.popup:
            self.popup.destroy()
            self.popup = None
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
