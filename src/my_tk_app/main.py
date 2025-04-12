# 入口程式，啟動主視窗與應用程式

from src.my_tk_app.controller.main_controller import MainController

if __name__ == '__main__':
    app = MainController()
    app.run()

