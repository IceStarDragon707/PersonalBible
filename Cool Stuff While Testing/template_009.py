import tkinter as tk
from tkinter import ttk

def change_listbox_fontsize(listbox, new_font_size):
    listbox.config(font=("Arial", new_font_size))

def change_combobox_fontsize(combobox, new_font_size):
    combobox.config(font=("Arial", new_font_size))

def change_fontsize(font_size):
    change_listbox_fontsize(listbox, font_size)
    change_combobox_fontsize(combobox, font_size)

root = tk.Tk()
root.title("Change Elements Fontsize Example")

default_elements = ["Item 1", "Item 2", "Item 3"]
listbox = tk.Listbox(root, listvariable=tk.StringVar(value=default_elements))
listbox.pack()

combobox = ttk.Combobox(root, values=default_elements)
combobox.pack(padx=20, pady=5)

font_size_label = tk.Label(root, text="Font Size:")
font_size_label.pack()

font_size_var = tk.StringVar()
font_size_var.set("12")
font_size_entry = tk.Entry(root, textvariable=font_size_var)
font_size_entry.pack()


listbox_fontsize_button = tk.Button(
    root, text="Change Listbox Fontsize",
    command=lambda: change_listbox_fontsize(listbox, int(font_size_entry.get()))
)
listbox_fontsize_button.pack(pady=5)

combobox_fontsize_button = tk.Button(
    root, text="Change Combobox Fontsize",
    # command=lambda: change_combobox_fontsize()
    command=lambda: change_combobox_fontsize(combobox, int(font_size_var.get()))
)
combobox_fontsize_button.pack(pady=5)


fontsize_slider = tk.Scale(root, from_=8, to=20, orient=tk.HORIZONTAL, label="Font Size",command=lambda value: change_fontsize(value))
fontsize_slider.pack(padx=20, pady=5)


root.mainloop()
