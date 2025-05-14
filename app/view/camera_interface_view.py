from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QComboBox, QGroupBox, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QProgressBar, QSpinBox, QFormLayout


class CameraInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('相機控制介面')
        self.setGeometry(100, 100, 400, 500)
        
        # 設定視窗背景為白色
        self.setStyleSheet("background-color: white;")
        
        # 建立中央 widget 和主要佈局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        
        # 標題
        title_label = QLabel('相機控制面板')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #333333;")
        main_layout.addWidget(title_label)
        
        # 相機控制群組
        camera_group = QGroupBox('相機控制')
        camera_group.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                color: #495057;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        camera_layout = QVBoxLayout()
        
        # 開啟相機按鈕
        self.open_camera_btn = QPushButton('開啟相機')
        self.open_camera_btn.setMinimumHeight(50)
        self.open_camera_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        camera_layout.addWidget(self.open_camera_btn)
        
        # 選擇鏡頭選單
        camera_selection_layout = QHBoxLayout()
        camera_label = QLabel('選擇鏡頭:')
        camera_label.setStyleSheet("color: #495057; font-weight: normal;")
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(['前置鏡頭', '後置鏡頭', '廣角鏡頭', 'USB相機'])
        self.camera_combo.setMinimumHeight(35)
        self.camera_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 5px;
                color: #495057;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #495057;
                margin-right: 5px;
            }
            QComboBox:hover {
                border: 1px solid #80bdff;
            }
        """)
        camera_selection_layout.addWidget(camera_label)
        camera_selection_layout.addWidget(self.camera_combo)
        camera_layout.addLayout(camera_selection_layout)
        
        camera_group.setLayout(camera_layout)
        main_layout.addWidget(camera_group)
        
        # 影像設定群組
        image_group = QGroupBox('影像設定')
        image_group.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                color: #495057;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        image_layout = QVBoxLayout()
        
        # 解析度選擇
        resolution_layout = QHBoxLayout()
        resolution_label = QLabel('解析度:')
        resolution_label.setStyleSheet("color: #495057; font-weight: normal;")
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(['1920x1080 (Full HD)', 
                                      '1280x720 (HD)', 
                                      '640x480 (VGA)',
                                      '3840x2160 (4K)'])
        self.resolution_combo.setMinimumHeight(35)
        self.resolution_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 5px;
                color: #495057;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #495057;
                margin-right: 5px;
            }
            QComboBox:hover {
                border: 1px solid #80bdff;
            }
        """)
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolution_combo)
        image_layout.addLayout(resolution_layout)
        
        image_group.setLayout(image_layout)
        main_layout.addWidget(image_group)
        
        # 錄影控制群組
        recording_group = QGroupBox('錄影控制')
        recording_group.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                color: #495057;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        recording_layout = QVBoxLayout()
        
        # 儲存影片按鈕
        self.save_video_btn = QPushButton('開始錄影')
        self.save_video_btn.setMinimumHeight(45)
        self.save_video_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        recording_layout.addWidget(self.save_video_btn)
        
        # 存取時長設定
        duration_layout = QFormLayout()
        self.duration_label = QLabel('錄影時長(秒):')
        self.duration_label.setStyleSheet("color: #495057; font-weight: normal;")
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setMinimum(1)
        self.duration_spinbox.setMaximum(3600)  # 最多1小時
        self.duration_spinbox.setValue(60)  # 預設1分鐘
        self.duration_spinbox.setSuffix(' 秒')
        self.duration_spinbox.setMinimumHeight(35)
        self.duration_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 5px;
                color: #495057;
            }
            QSpinBox:hover {
                border: 1px solid #80bdff;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #f8f9fa;
                border: 1px solid #ced4da;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e9ecef;
            }
        """)
        duration_layout.addRow(self.duration_label, self.duration_spinbox)
        recording_layout.addLayout(duration_layout)
        
        recording_group.setLayout(recording_layout)
        main_layout.addWidget(recording_group)
        
        # 進度條
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat('就緒')
        self.progress_bar.setMinimumHeight(35)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                text-align: center;
                color: #495057;
                font-size: 14px;
            }
            QProgressBar::chunk {
                background-color: #28a745;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # 新增彈性空間，將元件向上推
        main_layout.addStretch()
        
        # 連接信號 (這裡只是示例，實際功能需要額外實作)
        self.open_camera_btn.clicked.connect(self.on_open_camera)
        self.save_video_btn.clicked.connect(self.on_save_video)
        
    def on_open_camera(self):
        # 這裡放置開啟相機的程式碼
        if self.open_camera_btn.text() == '開啟相機':
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat('相機已開啟')
            self.open_camera_btn.setText('關閉相機')
        else:
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat('就緒')
            self.open_camera_btn.setText('開啟相機')
    
    def on_save_video(self):
        # 這裡放置儲存影片的程式碼
        if self.save_video_btn.text() == '開始錄影':
            self.save_video_btn.setText('停止錄影')
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat(f'正在錄影... 0%')
            # 這裡可以加入定時器來更新進度條
        else:
            self.save_video_btn.setText('開始錄影')
            self.progress_bar.setValue(100)
            self.progress_bar.setFormat('錄影已完成並儲存')


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    camera_interface = CameraInterface()
    camera_interface.show()
    sys.exit(app.exec())