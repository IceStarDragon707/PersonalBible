import tkinter as tk
from tkinter import ttk, filedialog

def save_text_to_file():
    text_content = text_widget.get("1.0", tk.END)
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        initialfile="custom_file_name.txt",  # Customize default filename
        initialdir="C:/Users/YourUsername/Documents"  # Set initial directory
    )
    
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_content)

root = tk.Tk()
root.title("Save Text to File")

text_widget = tk.Text(root)
text_widget.pack(padx=20, pady=10)

save_button = tk.Button(root, text="Save to File", command=save_text_to_file)
save_button.pack(pady=10)

root.mainloop()
