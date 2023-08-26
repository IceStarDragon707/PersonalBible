import tkinter as tk

def on_entry_change(P, V, reason):
    print("Entry value changed:", V.get())

root = tk.Tk()
root.title("Entry Value Change")

entry_var = tk.StringVar()
entry_var.trace_add("write", lambda *args: on_entry_change(entry, entry_var, "write"))

entry = tk.Entry(root, textvariable=entry_var)
entry.pack(padx=20, pady=10)

root.mainloop()
