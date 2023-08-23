import tkinter as tk

def open_sub_window():
    sub_window = tk.Toplevel(root)
    sub_window.title("Sub Window")

root = tk.Tk()
root.title("Main Window")

open_sub_button = tk.Button(root, text="Open Sub Window", command=open_sub_window)
open_sub_button.pack()

root.mainloop()
