import json
import tkinter as tk
from tkinter import *
from interface import Interface
from config import Member
from logic import Logic

palette = {
    1: "#558B57",
    2: "#83AF7E",
    3: "#E0F7CB",
    4: "#B1D2A3",
    5: "#276733",
    6: "#5EBC61",
    7: "#4D9B50"
}


def read_participants():
    with open("config.json") as f:
        pcps = json.load(f)
    pcps_full = {}
    for p in pcps:
        pcps_full[p] = Member(pcps[p]["name"], pcps[p]["family_id"], pcps[p]["age"], pcps[p]["exceptions"])
    return pcps_full


participants = read_participants()
adults = {name: member for name, member in participants.items() if member.age == "adult"}
children = {name: member for name, member in participants.items() if member.age == "child"}

if __name__ == "__main__":
    lgc = Logic(adults, children)
    root = tk.Tk()
    
    itf = Interface(lgc.run, read_participants, participants, root)
    root.mainloop()

    # root = PanedWindow()
    # root.mainloop()

    # m1 = PanedWindow()
    # m1.pack(fill=BOTH, expand=1)

    # left = Entry(m1, bd=5)
    # m1.add(left)

    # m2 = PanedWindow(m1, orient=VERTICAL)
    # m1.add(m2)

    # top = Scale( m2, orient=HORIZONTAL)
    # m2.add(top)

    # bottom = Button(m2, text="OK")
    # m2.add(bottom)

    # mainloop()
