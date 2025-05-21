import sys
from PyQt6 import QtWidgets, QtGui, QtCore

#===== 標籤設定 =====#
def label_setup(text, font_Set):
    label = QtWidgets.QLabel(text)
    label.setStyleSheet(f"{font_Set}; border: 0px;  color: rgb(0, 0, 0 )")
    # label.setFixedWidth(100)
    return label

#===== 輸入框設定 =====# 
def entry_setup(prompt_text, font_Set):
    entry = QtWidgets.QLineEdit()
    entry.setPlaceholderText(prompt_text)  # 設定提示文字
    entry.setStyleSheet(f"{font_Set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px; color: rgb(0, 0, 0)")  # 設定字型大小
    return entry

#===== 下拉選單設定 =====#
def combobox_setup(items, font_set):
    comboBox = QtWidgets.QComboBox()
    comboBox.setStyleSheet(f'{font_set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px; color: rgb(0, 0, 0)')  # 設定字型大小
    comboBox.addItems(items)
    comboBox.setCurrentIndex(0)  # 設定預設選項
    return comboBox

#===== 日期選擇器設定 =====#
def date_setup(Form, font_Set):
    date = QtWidgets.QDateEdit(Form)  # 建立日期調整元件
    date.setDisplayFormat('yyyy-MM-dd')  # 設定顯示格式
    date.setDate(QtCore.QDate.currentDate())
    date.setKeyboardTracking(False)
    date.setCalendarPopup(True)  # 設定為彈出式日曆
    date.setStyleSheet(f'{font_Set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px; color: rgb(0, 0, 0)')  # 設定字型大小
    
    
    return date

def button_setup(text, connect_function):
    button = QtWidgets.QPushButton(text)
    button.clicked.connect(connect_function)  # 連結按鈕點擊事件
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: rgb(255, 255, 255);
            color: rgb(0, 0, 0);
            border: 1.5px solid black;
            border-radius: 8px;
            text-align: center;
            font-family: "微軟正黑體";
            font-size: 20px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: rgb(174, 214, 241);
        }}
        QPushButton:pressed {{
            background-color: rgb(30, 144, 255);
            color: rgb(255, 255, 255);
            border: 1.5px dashed black;
            
        }}
    """)

    return button