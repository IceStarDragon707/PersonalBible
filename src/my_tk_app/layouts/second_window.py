# 第二視窗示例，同樣繼承 BaseView

# views/second_window.py
import tkinter as tk
from tkinter import ttk
from src.my_tk_app.layouts.base_view import BaseView


class SecondWindow(BaseView):
    def create_widgets(self):
        self.info = ttk.Label(self.root, text="This is the second window!")

    def set_layout(self):
        self.info.pack(padx=20, pady=20)

