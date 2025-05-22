from PyQt6 import QtWidgets, QtCore, QtGui
from widget_helper import label_setup, entry_setup, button_setup
import sys


class CameraWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拍攝視窗")
        self.resize(900, 700)
        self.setStyleSheet("background-color: rgb(248, 249, 250);")
        self.save_path = {}
        self.ui()
        


    def ui(self):
        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        #==== Create first layout ====#
        self.grid1_box = QtWidgets.QWidget()
        self.grid1_box.setStyleSheet("")
        self.grid1_layout = QtWidgets.QHBoxLayout(self.grid1_box)
        self.title_label = label_setup("Camera", lambda: None)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: rgb(0, 0, 0); border: 0px;")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.grid1_layout.addWidget(self.title_label)

        self.main_layout.addWidget(self.grid1_box)
        #==== Finish ====#
        
        #==== Create second layout ====#
        self.layout2_box = QtWidgets.QWidget()
        self.layout2_box.setStyleSheet("")
        self.layout2_layout = QtWidgets.QHBoxLayout(self.layout2_box)

        self.camera_frame = QtWidgets.QFrame()
        self.camera_frame.setStyleSheet("background-color: rgb(51, 51, 51); border-radius: 8px; ")
        self.camera_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel) # 畫矩形面板，會依據目前的GUI主題自動調整
        self.camera_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        
        self.camera_layout = QtWidgets.QVBoxLayout(self.camera_frame)
        self.camera_layout.setContentsMargins(10, 10, 10, 10)
        
        self.camera_label = label_setup("", lambda: None)
        self.camera_label.setStyleSheet("background-color: black; border-radius: 4px;")
        self.camera_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setMinimumHeight(500)
        self.camera_layout.addWidget(self.camera_label)
        
        self.layout2_layout.addWidget(self.camera_frame)

        self.main_layout.addWidget(self.layout2_box)
        #==== Finish ====#
        
        
        #==== Create third layout ====#
        self.entry_folder_frame = QtWidgets.QFrame()
        self.entry_folder_layout = QtWidgets.QHBoxLayout(self.entry_folder_frame)
        self.entry_folder_entry = QtWidgets.QLineEdit()
        self.entry_folder_entry.setPlaceholderText("請選擇儲存資料夾")  # 設定提示文字
        self.entry_folder_entry.setStyleSheet("background-color: rgb(255, 255, 255); border: 1.5px solid black; border-radius: 5px; color: rgb(0, 0, 0);" \
        "font-size: 18px; font-family: 微軟正黑體; font-weight: bold")  # 設定字型大小
        self.entry_folder_entry.setReadOnly(True)  # Set the entry to read-only
        self.entry_folder_layout.addWidget(self.entry_folder_entry)

        self.main_layout.addWidget(self.entry_folder_frame)
        #==== Finish ====#
        

        #==== Create fourth layout ====#
        self.button_frame = QtWidgets.QFrame()
        # self.button_frame.setStyleSheet("background-color: #e0e0e0; border-radius: 8px;")
        self.button_layout = QtWidgets.QHBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        # self.button_layout.setSpacing(15)
        
        
        # Previous button
        self.prev_button = button_setup("上一步", lambda: None)
        self.button_layout.addWidget(self.prev_button)
        
        # Stop recording button
        self.save_button = button_setup("選擇儲存資料夾", lambda: None)
        # self.stop_button.setEnabled(False)  # Initially disabled
        self.button_layout.addWidget(self.save_button)
        self.save_path['save_path'] = self.save_button
        


        # Record button
        self.record_button = button_setup("開始錄影", lambda: None)
        self.button_layout.addWidget(self.record_button)
        
        
        # Next button
        self.next_button = button_setup("下一步", lambda: None)
        self.button_layout.addWidget(self.next_button)
        
        # Add buttons frame to main layout
        self.main_layout.addWidget(self.button_frame)


        

  
            

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = CameraWindow()
    Form.show()
    sys.exit(app.exec())