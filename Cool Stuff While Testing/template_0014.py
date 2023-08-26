import tkinter as tk

def delete_item():
    selected_index = listbox.curselection()
    if selected_index:
        listbox.delete(selected_index)

def rename_item():
    selected_index = listbox.curselection()
    if selected_index:
        new_name = entry.get()
        if new_name:
            listbox.delete(selected_index)
            listbox.insert(selected_index, new_name)

root = tk.Tk()
root.title("Listbox Manipulation")

listbox = tk.Listbox(root)
listbox.pack(padx=20, pady=10)

initial_items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
for item in initial_items:
    listbox.insert(tk.END, item)

delete_button = tk.Button(root, text="Delete Selected", command=delete_item)
delete_button.pack(pady=5)

rename_button = tk.Button(root, text="Rename Selected", command=rename_item)
rename_button.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

root.mainloop()
