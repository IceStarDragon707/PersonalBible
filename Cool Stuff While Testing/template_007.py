import tkinter as tk

def on_resize(event):
    width = sub_window.winfo_width()
    height = sub_window.winfo_height()
    size_label.config(text=f"Width: {width}, Height: {height}")

root = tk.Tk()
root.title("Main Window")

sub_window = tk.Toplevel(root)
sub_window.title("Resizable Sub Window")
sub_window.geometry("300x200")  # Initial size

size_label = tk.Label(sub_window, text="Width: 300, Height: 200")
size_label.pack(padx=20, pady=10)

sub_window.bind("<Configure>", on_resize)  # Bind resize event

root.mainloop()
