# 視窗基底類別，封裝通用初始化、佈局、事件綁定等

# views/base_view.py
import tkinter as tk
from tkinter import ttk

from src.my_tk_app.config import load_config

class BaseView:
    def __init__(self, title="Application", geometry="800x600"):
        self.root = tk.Tk() if not hasattr(self, "root") else self.root
        self.root.title(title)
        self.root.geometry(geometry)
        self.setup_style()
        self.create_widgets()
        self.set_layout()

        self.config = load_config()
        self.root = tk.Tk()
        self.root.title(self.config["window"]["title"])
        self.root.geometry(self.config["window"]["geometry"])

    def setup_style(self):
        # 統一設置樣式，若需要使用ttk主題等
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')  # 示例主題

    def create_widgets(self):
        # 子類別實作各自的組件建立
        pass

    def set_layout(self):
        # 子類別設定組件佈局，統一使用 layout_helper 可調整padding/sticky 等
        pass

    def start(self):
        self.root.mainloop()
