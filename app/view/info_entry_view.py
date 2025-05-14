from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox, 
    QDateEdit,
    QFrame, 
    QGridLayout, 
    QGroupBox, 
    QHBoxLayout,
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QScrollArea, 
    QVBoxLayout, 
    QWidget, 
)


class InfoEntryPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        # 基本設定
        self.setWindowTitle("個人資料")
        self.resize(450, 700)
        self.setMinimumSize(450, 500)
        
        # 設定主題色彩
        self.setStyleSheet("background-color: white;")
        
        # 建立主要佈局（這個佈局會包含滾動區域）
        self.window_layout = QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        
        # 建立滾動區域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 設定滾動條樣式
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # 建立內容容器
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: white;")
        
        # 將原本的 main_layout 設定給內容容器
        self.main_layout = QVBoxLayout(self.content_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # 將內容容器設定給滾動區域
        self.scroll_area.setWidget(self.content_widget)
        
        # 將滾動區域加入主視窗佈局
        self.window_layout.addWidget(self.scroll_area)
        
        # 建立 UI 元件
        self.create_widgets()
    
    def create_label(self, text):
        """建立標籤"""
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 15px;
                font-weight: normal;
                padding: 5px;
            }
        """)
        return label
    
    def create_entry(self, placeholder=""):
        """建立輸入框"""
        entry = QLineEdit()
        entry.setPlaceholderText(placeholder)
        entry.setMinimumHeight(38)
        entry.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #495057;
            }
            QLineEdit:hover {
                border: 1px solid #80bdff;
            }
            QLineEdit:focus {
                border: 2px solid #007bff;
                outline: none;
            }
        """)
        return entry
    
    def create_combobox(self, items):
        """建立下拉式選單"""
        combo = QComboBox()
        combo.addItems(items)
        combo.setMinimumHeight(38)
        combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
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
                margin-right: 8px;
            }
            QComboBox:hover {
                border: 1px solid #80bdff;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #ced4da;
                selection-background-color: #e3f2fd;
            }
        """)
        return combo
    
    def create_group_box(self, title):
        """建立群組框"""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
                font-size: 16px;
                font-weight: bold;
                color: #343a40;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: white;
                border-radius: 5px;
            }
        """)
        return group
    
    def create_widgets(self):
        """建立所有的UI元件"""
        # 標題
        title_label = QLabel('個人資料登記表')
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; padding: 15px; background-color: #f8f9fa; border-radius: 10px;")
        self.main_layout.addWidget(title_label)
        
        # 儲存所有的輸入元件
        self.entries = {}
        
        # 基本資料群組
        basic_group = self.create_group_box('基本資料')
        basic_layout = QGridLayout()
        basic_layout.setSpacing(15)
        
        # 編號和性別
        basic_layout.addWidget(self.create_label('編號：'), 0, 0)
        self.entries['id'] = self.create_entry('請輸入編號')
        basic_layout.addWidget(self.entries['id'], 0, 1)
        
        basic_layout.addWidget(self.create_label('性別：'), 0, 2)
        self.entries['gender'] = self.create_combobox(['請選擇性別', '男', '女', '其他'])
        self.entries['gender'].setStyleSheet(
            """
            font-size: 15; font-weight:normal; color:#495057; 
            background-color: rgb(255, 255, 255); border-radius: 5px;
            """
        )
        basic_layout.addWidget(self.entries['gender'], 0, 3)
        
        # 年齡和生日
        basic_layout.addWidget(self.create_label('年齡：'), 1, 0)
        self.entries['age'] = self.create_entry('請輸入年齡')
        basic_layout.addWidget(self.entries['age'], 1, 1)
        
        basic_layout.addWidget(self.create_label('生日：'), 1, 2)
        self.entries['birthday'] = QDateEdit()
        self.entries['birthday'].setDisplayFormat('yyyy/MM/dd')
        self.entries['birthday'].setCalendarPopup(True)
        self.entries['birthday'].setDate(QDate.currentDate())
        self.entries['birthday'].setMinimumHeight(38)
        self.entries['birthday'].setKeyboardTracking(True)
        self.entries['birthday'].setStyleSheet(
            """
            font-weight:normal; color:#495057; 
            background-color: rgb(255, 255, 255); border-radius: 5px;
            """
        )
        self.entries['birthday'].setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter) 
        basic_layout.addWidget(self.entries['birthday'], 1, 3)
        
        basic_layout.addWidget(self.create_label('身高:'), 2, 0)
        self.entries['height'] = self.create_entry('請輸入身高')
        basic_layout.addWidget(self.entries['height'], 2, 1)

        basic_layout.addWidget(self.create_label('體重:'), 2, 2)
        self.entries['weight'] = self.create_entry('請輸入體重')
        basic_layout.addWidget(self.entries['weight'], 2, 3)

        basic_layout.addWidget(self.create_label('聯絡電話：'), 3, 0)
        self.entries['phone'] = self.create_entry('請輸入聯絡電話')
        basic_layout.addWidget(self.entries['phone'], 3, 1)

        # 設定列寬比例
        basic_layout.setColumnStretch(0, 1)
        basic_layout.setColumnStretch(1, 3)
        basic_layout.setColumnStretch(2, 1)
        basic_layout.setColumnStretch(3, 3)
        
        basic_group.setLayout(basic_layout)
        self.main_layout.addWidget(basic_group)
        
        # 拍攝資訊群組
        shooting_group = self.create_group_box('拍攝資訊')
        shooting_layout = QGridLayout()
        shooting_layout.setSpacing(15)
        
        shooting_layout.addWidget(self.create_label('拍攝日期：'), 0, 0)
        self.entries['shooting_date'] = QDateEdit()
        self.entries['shooting_date'].setDisplayFormat('yyyy/MM/dd')
        self.entries['shooting_date'].setCalendarPopup(True)
        self.entries['shooting_date'].setDate(QDate.currentDate())
        self.entries['shooting_date'].setMinimumHeight(38)
        self.entries['shooting_date'].setKeyboardTracking(True)
        self.entries['shooting_date'].setStyleSheet(
            """
            font-weight:normal; color:#495057; 
            background-color: rgb(255, 255, 255); border-radius: 5px;
            """
        )
        shooting_layout.addWidget(self.entries['shooting_date'], 0, 1, 1, 3)
        
        self.entries['reason'] = self.create_combobox(['請選擇拍攝原因', '醫療', '健檢', '其他'])
        self.entries['reason'].setStyleSheet(
            """
            font-size: 15; font-weight:normal; color:#495057; 
            background-color: rgb(255, 255, 255); border-radius: 5px;
            """
        )
        shooting_layout.addWidget(self.create_label('拍攝原因：'), 1, 0)
        shooting_layout.addWidget(self.entries['reason'], 1, 1, 1, 3)

        self.entries['shooting_location'] = self.create_entry('請輸入拍攝地點')
        shooting_layout.addWidget(self.create_label('拍攝地點：'), 2, 0)
        shooting_layout.addWidget(self.entries['shooting_location'], 2, 1, 1, 3)

        shooting_layout.setColumnStretch(0, 1)
        shooting_layout.setColumnStretch(1, 5)
        
        shooting_group.setLayout(shooting_layout)
        self.main_layout.addWidget(shooting_group)
        
        # 醫療資訊群組
        medical_group = self.create_group_box('醫療資訊')
        medical_layout = QGridLayout()
        medical_layout.setSpacing(15)
        
        # 病史
        medical_layout.addWidget(self.create_label('病史：'), 0, 0)
        self.entries['medical_history'] = self.create_entry('請輸入病史')
        medical_layout.addWidget(self.entries['medical_history'], 0, 1)
        
        # 過敏史
        medical_layout.addWidget(self.create_label('過敏史：'), 1, 0)
        self.entries['allergy_history'] = self.create_entry('請輸入過敏史')
        medical_layout.addWidget(self.entries['allergy_history'], 1, 1)

        # 目前用藥
        medical_layout.addWidget(self.create_label('目前用藥：'), 2, 0)
        self.entries['current_medication'] = self.create_entry('請輸入目前服用藥物')
        medical_layout.addWidget(self.entries['current_medication'], 2, 1)

        # 注意事項
        medical_layout.addWidget(self.create_label('注意事項：'), 3, 0)
        self.entries['notes'] = self.create_entry('請輸入注意事項')
        medical_layout.addWidget(self.entries['notes'], 3, 1)
        
        medical_group.setLayout(medical_layout)
        self.main_layout.addWidget(medical_group)
        
        # 按鈕區域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # 清除按鈕
        clear_btn = QPushButton('清除資料')
        clear_btn.setMinimumHeight(40)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 8px 30px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        clear_btn.clicked.connect(self.clear_data)
        
        # 儲存按鈕
        save_btn = QPushButton('儲存資料')
        save_btn.setMinimumHeight(40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 8px 30px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(save_btn)
        button_layout.addStretch()
        
        self.main_layout.addLayout(button_layout)
        
        # 添加彈性空間
        self.main_layout.addStretch()
    
    def get_data(self):
        """獲取所有輸入資料"""
        data = {}
        for key, widget in self.entries.items():
            if isinstance(widget, QLineEdit):
                data[key] = widget.text()
            elif isinstance(widget, QComboBox):
                data[key] = widget.currentText()
        return data
    
    def set_data(self, data):
        """設定所有輸入資料"""
        for key, value in data.items():
            if key in self.entries:
                widget = self.entries[key]
                if isinstance(widget, QLineEdit):
                    widget.setText(str(value))
                elif isinstance(widget, QComboBox):
                    index = widget.findText(str(value))
                    if index >= 0:
                        widget.setCurrentIndex(index)
    
    def clear_data(self):
        """清除所有輸入資料"""
        for widget in self.entries.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
            else:
                widget.clear()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = InfoEntryPanel()
    window.show()
    sys.exit(app.exec())