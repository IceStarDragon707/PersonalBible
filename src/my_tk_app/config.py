# 配置讀取模組，統一管理 GUI 參數、樣式設定

# config.py
import json
import os

def load_config(config_file='config.json'):
    if os.path.exists(config_file):
        with open(config_file, encoding='utf-8') as f:
            return json.load(f)
    else:
        # 返回一些默認配置
        return {
            "window": {"title": "My Tkinter App", "geometry": "800x600"},
            "layout": {"padx": 10, "pady": 10, "sticky": "nsew"},
            "style": {"theme": "clam"}
        }

