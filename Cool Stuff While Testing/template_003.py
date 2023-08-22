import tkinter as tk

def increase_font_size():
    global current_font_size
    current_font_size += 2
    update_label_font()

def decrease_font_size():
    global current_font_size
    current_font_size -= 2
    update_label_font()

def update_label_font():
    label.config(font=("Arial", current_font_size))

current_font_size = 12

root = tk.Tk()
root.title("Label Font Size Modification")

label = tk.Label(root, text="Change Font Size", font=("Arial", current_font_size))
label.pack()

increase_button = tk.Button(root, text="Increase Font Size", command=increase_font_size)
increase_button.pack()

decrease_button = tk.Button(root, text="Decrease Font Size", command=decrease_font_size)
decrease_button.pack()

root.mainloop()
