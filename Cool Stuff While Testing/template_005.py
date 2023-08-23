import tkinter as tk
from tkinter import ttk

class SubWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sub Window")
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        self.div_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.div_frame, text="Div")
        
        self.button1 = ttk.Button(self.div_frame, text="Button 1")
        self.button2 = ttk.Button(self.div_frame, text="Button 2")
        self.combobox1 = ttk.Combobox(self.div_frame, values=["Option 1", "Option 2"])
        self.combobox2 = ttk.Combobox(self.div_frame, values=["Option A", "Option B"])
        
        self.button1.pack(padx=10, pady=5)
        self.button2.pack(padx=10, pady=5)
        self.combobox1.pack(padx=10, pady=5)
        self.combobox2.pack(padx=10, pady=5)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        
        self.sub_window = None
        
        self.open_sub_window_button = tk.Button(self, text="Open Sub Window", command=self.open_sub_window)
        self.open_sub_window_button.pack(padx=20, pady=10)
        
    def open_sub_window(self):
        if self.sub_window is None or not self.sub_window.winfo_exists():
            self.sub_window = SubWindow(self)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
