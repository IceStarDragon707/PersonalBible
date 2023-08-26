import tkinter as tk
from tkinter import ttk

def on_entry_click(event):
    if entry_var.get() == hint_text:
        entry_var.set("")
        entry.config(foreground="black")

def on_entry_leave(event):
    if entry_var.get() == "":
        entry_var.set(hint_text)
        entry.config(foreground="gray")

root = tk.Tk()
root.title("Entry with Hint Text")

hint_text = "Enter text here"

style = ttk.Style()

# Create a custom style for the Entry widget
style.configure("Hint.TEntry", foreground="gray")
style.map("Hint.TEntry", foreground=[("focus", "black"), ("!focus", "gray")])

entry_var = tk.StringVar()
entry_var.set(hint_text)

entry = ttk.Entry(root, textvariable=entry_var, style="Hint.TEntry")
entry.pack(padx=20, pady=10)

entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_entry_leave)

root.mainloop()
