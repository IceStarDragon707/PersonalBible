import tkinter as tk
from tkinter import ttk

def add_item():
    new_item = entry.get()
    if new_item:
        items.append(new_item)
        update_combobox()

def update_combobox():
    combobox["values"] = items
    entry.delete(0, tk.END)  # Clear the entry widget

# Create the main window
root = tk.Tk()
root.title("Dynamic ComboBox Example")

# Create a Combobox widget
combobox = ttk.Combobox(root)
combobox.pack()

# Entry widget to add new items
entry = ttk.Entry(root)
entry.pack()

# Button to add new items
add_button = ttk.Button(root, text="Add Item", command=add_item)
add_button.pack()

# Initialize the items list
items = ["Item 1", "Item 2", "Item 3"]

# Set initial values for the ComboBox
update_combobox()

# Start the Tkinter main loop
root.mainloop()
