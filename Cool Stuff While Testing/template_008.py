import tkinter as tk

root = tk.Tk()
root.title("Text Widget with Color")

text_widget = tk.Text(root)
text_widget.pack(padx=20, pady=10)

# Insert text with color tags
text_widget.insert("insert", "Hello, ", ("normal",))
text_widget.insert("insert", "Colored ", ("colored",))
text_widget.insert("insert", "World!", ("normal",))

# Configure tag for normal text (black color)
text_widget.tag_configure("normal", foreground="black")

# Configure tag for colored text (red color)
text_widget.tag_configure("colored", foreground="red")

root.mainloop()
