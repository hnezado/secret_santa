import tkinter as tk
from tkinter import ttk
import random
import string

class SantaGPTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SantaGPT")
        
        self.tabControl = ttk.Notebook(self.root)
        self.tab_run = ttk.Frame(self.tabControl)
        self.tab_config = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.tab_run, text='Run')
        self.tabControl.add(self.tab_config, text='Configuration')
        
        self.tabControl.pack(expand=1, fill='both')
        
        self.create_run_tab()
    
    def create_run_tab(self):
        self.table = ttk.Treeview(self.tab_run, columns=('ID', 'Nombre', 'Relación', 'Excluídos'), show='headings')
        self.table.heading('ID', text='ID')
        self.table.heading('Nombre', text='Nombre')
        self.table.heading('Relación', text='Relación')
        self.table.heading('Excluídos', text='Excluídos')
        
        self.table.pack(fill='both', expand=1)
        
        self.run_button = tk.Button(self.tab_run, text='Run', command=self.generate_data)
        self.clear_button = tk.Button(self.tab_run, text='Clear', command=self.clear_table)
        
        self.run_button.pack(side='left', fill='x', expand=1)
        self.clear_button.pack(side='left', fill='x', expand=1)
    
    def generate_data(self):
        self.clear_table()
        num_rows = random.randint(5, 10)
        for i in range(num_rows):
            id_num = i + 1
            name = ''.join(random.choices(string.ascii_letters, k=6))  # Nombre aleatorio de 6 letras
            relations = ', '.join(random.choices(string.ascii_uppercase, k=random.randint(1, 3)))  # Relaciones aleatorias
            excluded = ', '.join(random.choices(string.ascii_uppercase, k=random.randint(0, 3)))  # Excluídos aleatorios
            self.table.insert('', 'end', values=(id_num, name, relations, excluded))
    
    def clear_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

def main():
    root = tk.Tk()
    app = SantaGPTApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
