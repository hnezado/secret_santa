import tkinter as tk
from tkinter import ttk

root = tk.Tk()

def display(mode, pack_mode):
    root.geometry("640x480")
    notebook = ttk.Notebook(root)
    column_names = ("group", "name", "year")
    
    if mode == "tab":
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Data")
        treeview_data = ttk.Treeview(frame)
        treeview_data.configure(columns=column_names)
        treeview_data.heading("#0", text="ID")
        [treeview_data.heading(col, text=col.title()) for col in column_names]
        treeview_data.pack(fill=tk.BOTH, expand=True)
    elif mode == "root":
        frame = tk.Frame(root)
        
    if pack_mode == "both":
        notebook.pack(fill=tk.BOTH, expand=True)
    elif pack_mode == 2:
        notebook.pack()

        

display("tab", "both")
root.mainloop()
