# 統一管理 sticky、padx、pady 等設定的輔助模組

# utils/layout_helper.py

def grid_configure(widget, row, column, padx=5, pady=5, sticky="nsew"):
    widget.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

