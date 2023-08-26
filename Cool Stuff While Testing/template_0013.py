import tkinter as tk

root = tk.Tk()
root.title("Listbox with Different Text Colors")

listbox = tk.Listbox(root)
listbox.pack(padx=20, pady=10)

# Add elements with their associated text colors
elements = [("Item 1", "blue"), ("Item 2", "red"), ("Item 3", "green")]
for item, color in elements:
    listbox.insert(tk.END, item)
    listbox.itemconfig(tk.END, {'fg': color})

root.mainloop()
