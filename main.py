import json
from tkinter import *
from interface import Interface
from config import Member
from logic import Logic


def read_participants():
    with open("config.json") as f:
        pcps = json.load(f)
    pcps_full = {}
    for p in pcps:
        pcps_full[p] = Member(pcps[p]["name"], pcps[p]["family_id"], pcps[p]["age"], pcps[p]["exceptions"])
    return pcps_full


def run():
    print("Running!")


def clear():
    print("Clearing!")


def main():
    # participants = read_participants()
    # adults = {name: member for name, member in participants.items() if member.age == "adult"}
    # children = {name: member for name, member in participants.items() if member.age == "child"}
    
    # lgc = Logic(adults, children)
    # root = tk.Tk()
    # itf = Interface(lgc.run, read_participants, participants, root)
    # root.mainloop()
    
    app = Interface(style="./styles/santa_style.json", logic=(run, clear))
    app.display()


if __name__ == "__main__":
    main()

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
