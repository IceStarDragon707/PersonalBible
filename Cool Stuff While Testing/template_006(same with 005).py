import tkinter as tk
from tkinter import ttk

def open_sub_window():
    global sub_window
    if sub_window is None or not sub_window.winfo_exists():
        sub_window = tk.Toplevel(root)
        sub_window.title("Sub Window")
        
        notebook = ttk.Notebook(sub_window)
        notebook.pack(fill="both", expand=True)
        
        div_frame = ttk.Frame(notebook)
        notebook.add(div_frame, text="Div")
        
        button1 = ttk.Button(div_frame, text="Button 1")
        button2 = ttk.Button(div_frame, text="Button 2")
        combobox1 = ttk.Combobox(div_frame, values=["Option 1", "Option 2"])
        combobox2 = ttk.Combobox(div_frame, values=["Option A", "Option B"])
        
        button1.pack(padx=10, pady=5)
        button2.pack(padx=10, pady=5)
        combobox1.pack(padx=10, pady=5)
        combobox2.pack(padx=10, pady=5)

root = tk.Tk()
root.title("Main Window")

sub_window = None

open_sub_window_button = tk.Button(root, text="Open Sub Window", command=open_sub_window)
open_sub_window_button.pack(padx=20, pady=10)

root.mainloop()
