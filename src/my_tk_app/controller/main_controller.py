# 負責業務邏輯與事件處理，與 view 溝通

# controllers/main_controller.py
from src.my_tk_app.layouts.main_window import MainWindow


class MainController:
    def __init__(self):
        self.view = MainWindow(title="My Tkinter App", geometry="800x600")
        # 此處可以初始化資料模型, 配置管理等

    def run(self):
        # 綁定 view 中的事件與控制器方法，或由view自行呼叫controller
        self.view.start()


