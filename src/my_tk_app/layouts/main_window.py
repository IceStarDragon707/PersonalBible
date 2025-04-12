# 主視窗，繼承 BaseView，僅負責組件顯示與佈局

# views/main_window.py
import tkinter as tk
from tkinter import ttk
from src.my_tk_app.layouts.base_view import BaseView


class MainWindow(BaseView):
    def create_widgets(self):
        # 例如：建立一個按鈕、文字欄位等，純粹用於顯示與互動
        self.label = ttk.Label(self.root, text="Hello, Tkinter!")
        self.button = ttk.Button(self.root, text="Open Second Window", command=self.open_second_window)

    def set_layout(self):
        # 使用 grid / pack 來設定 layout (可引用 utils/layout_helper.py 封裝的統一設定)
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.button.grid(row=1, column=0, padx=10, pady=10)

    def open_second_window(self):
        # 通知 controller 或直接建立第二個視窗
        from src.my_tk_app.layouts.second_window import SecondWindow
        second_win = SecondWindow(title="Second Window", geometry="400x300")
        second_win.start()

