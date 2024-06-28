import Pmw
import tkinter as tk
from tkinter import ttk
from components.user_settings import *
from components.popup import Popup
from components.tab_run import Run
from components.tab_conf import Configuration
from components.tab_pref import Preferences


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
        self.root = tk.Tk()
        self.fixed_win = {
            "minsize": (640, 480),
            "dim": (800, 600),
            "pos": (0, 0)
        }
        self.set_root()
        self.pu = Popup(self)

        # Data
        self.img = {
            "add": tk.PhotoImage(file="images/add.png"),
            "edit": tk.PhotoImage(file="images/edit.png"),
            "del": tk.PhotoImage(file="images/del.png"),
            "checked": tk.PhotoImage(file="images/checked.png"),
            "unchecked": tk.PhotoImage(file="images/unchecked.png"),
            "en_flag": tk.PhotoImage(file="images/en.png"),
            "es_flag": tk.PhotoImage(file="images/es.png"),
            "fr_flag": tk.PhotoImage(file="images/fr.png"),
            "wip": tk.PhotoImage(file="images/wip.png")
        }

        # Components
        self.notebook = ttk.Notebook(self.root)
        self.tab_run = Run(self)
        self.tab_conf = Configuration(self)
        self.tab_pref = Preferences(self)

        Pmw.initialise(self.root)
        self.set_style()
        self.update_style()
        self.set_tabs()

    def update_lang(self, lang: str = None) -> None:
        """Updates the language data on the interface module"""

        def load_lang(language) -> dict:
            """Retrieves the selected language data"""
            with open("user_settings/lang.json", encoding="utf-8") as f:
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
        
        with open("user_settings/styles/static.json") as f:
            static = f.read()
            return json.loads(static)["grid"]

    @staticmethod
    def get_style_static() -> dict:
        """Retrieves the static style data"""
        
        with open("user_settings/styles/static.json") as f:
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
        self.tab_conf.create_tab()
        self.tab_pref.create_tab()
        self.notebook.grid(
            row=0,
            column=0,
            sticky=tk.NSEW
        )

    def update_tabs(self):
        """Updates every tab"""

        self.tab_run.update_tab()
        self.tab_conf.update_tab()
        self.tab_pref.update_tab()

    @staticmethod
    def disable_resizing(_) -> str:
        """Disables the column resizing"""

        return "break"

    def display(self) -> None:
        """Main interface"""

        self.tab_run.binds()
        self.tab_conf.binds()
        self.root.mainloop()
