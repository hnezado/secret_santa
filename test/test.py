import tkinter as tk
from tkinter import ttk

root = tk.Tk()

tree = ttk.Treeview(root, columns=('size', 'modified'), selectmode='browse')

tree.heading('size', text='SIZE')
tree.heading('modified', text='MODIFIED')

tree.insert('', "end", 'gallery1', text='Applications1')
tree.insert('', "end", 'gallery2', text='Applications2')

tree.selection_set('gallery1')

tree.focus_set()
tree.focus('gallery1')

tree.grid()
root.mainloop()