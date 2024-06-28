class Run:
    def __init__(self, ui):
        self.ui = ui

    def show(self):
        return self.ui.w


class Interface:
    def __init__(self):
        self.w = 800
        self.h = 600

        self.run_tab = Run(self)


ui = Interface()
print(ui.run_tab.show())