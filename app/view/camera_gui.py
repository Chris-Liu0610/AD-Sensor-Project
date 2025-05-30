import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget
)
from utils.widget_helper import label_setup, button_setup


class CameraWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拍攝視窗")
        self.resize(900, 700)
        self.setStyleSheet("background-color: rgb(248, 249, 250);")
        self.save_path = {}
        self.setup_ui()
        
    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        self.grid1_box = QWidget()
        self.grid1_box.setStyleSheet("")
        self.grid1_layout = QHBoxLayout(self.grid1_box)
        self.title_label = label_setup("Camera", lambda: None)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: rgb(0, 0, 0); border: 0px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid1_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.grid1_box)
        
        self.layout2_box = QWidget()
        self.layout2_box.setStyleSheet("")
        self.layout2_layout = QHBoxLayout(self.layout2_box)

        self.camera_frame = QFrame()
        self.camera_frame.setStyleSheet("background-color: rgb(51, 51, 51); border-radius: 8px; ")
        self.camera_frame.setFrameShape(QFrame.Shape.StyledPanel) 
        self.camera_frame.setFrameShadow(QFrame.Shadow.Raised)
        
        self.camera_layout = QVBoxLayout(self.camera_frame)
        self.camera_layout.setContentsMargins(10, 10, 10, 10)
        
        self.camera_label = label_setup("", lambda: None)
        self.camera_label.setStyleSheet("background-color: black; border-radius: 4px;")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setMinimumHeight(500)
        self.camera_layout.addWidget(self.camera_label)

        self.layout2_layout.addWidget(self.camera_frame)
        self.main_layout.addWidget(self.layout2_box)

        self.entry_folder_frame = QFrame()
        self.entry_folder_layout = QHBoxLayout(self.entry_folder_frame)
        self.entry_folder_entry = QLineEdit()
        self.entry_folder_entry.setPlaceholderText("請選擇儲存資料夾")  
        self.entry_folder_entry.setStyleSheet("background-color: rgb(255, 255, 255); border: 1.5px solid black; border-radius: 5px; color: rgb(0, 0, 0);" \
        "font-size: 18px; font-family: 微軟正黑體; font-weight: bold")  
        self.entry_folder_entry.setReadOnly(True)  
        self.entry_folder_layout.addWidget(self.entry_folder_entry)
        self.main_layout.addWidget(self.entry_folder_frame)

        self.button_frame = QFrame()
        self.button_layout = QHBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(10, 10, 10, 10)

        self.back_button = button_setup("上一步", lambda: None)
        self.button_layout.addWidget(self.back_button)
        
        self.save_button = button_setup("選擇儲存資料夾", lambda: None)
        self.button_layout.addWidget(self.save_button)
        self.save_path['save_path'] = self.save_button
        
        self.record_button = button_setup("開始錄影", lambda: None)
        self.button_layout.addWidget(self.record_button)
        
        self.finish_button = button_setup("完成", lambda: None)
        self.button_layout.addWidget(self.finish_button)
        
        self.main_layout.addWidget(self.button_frame)
