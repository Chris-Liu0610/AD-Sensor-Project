import sys


from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QGridLayout, 
    QWidget, 
    QFrame,
    QLabel, 
    QLineEdit, 
    QComboBox,
    QVBoxLayout,
    QGraphicsView,
    QGraphicsScene,
    QTabWidget
)



class ImageViewer(QLabel):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(QSize(640, 480))
        self.setFrameShape(QFrame.Shape.Box)
        self.setStyleSheet("background-color: #000;")
        self.setText("No Camera Feed")
        self.setScaledContents(False) 
        self.original_pixmap = None

    def resizeEvent(self, event):
        """Handle resize events to scale the image appropriately."""
        super().resizeEvent(event)
        if self.original_pixmap is not None:
            self.setPixmap(self._scale_pixmap())
    
    def _scale_pixmap(self):
        """Scale the pixmap to fit the widget while maintaining aspect ratio."""
        if self.original_pixmap is None:
            return QPixmap()
            
        return self.original_pixmap.scaled(
            self.width(), 
            self.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
    
    def update_view(self, frame):
        """Update the displayed frame.
        
        Args:
            frame: NumPy array containing the image data (BGR format)
        """
        if frame is None:
            self.setText("No Camera Feed")
            self.original_pixmap = None
            return
        # Update pixmap from the QImage
        self.original_pixmap = self._narr2pixmap(frame)
        # Apply scaled pixmap
        self.setPixmap(self._scale_pixmap())

    @staticmethod
    def _narr2pixmap(narr): 
        height, width, channel = narr.shape
        q_img = QImage(narr.data, width, height, channel * width, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(q_img)


    


class InfoEntryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        # 基本設定
        self.setWindowTitle("個人資料")
        self.resize(800, 450)  # 使用resize而不是setFixedSize
        self.setMinimumSize(600, 350)  # 設定最小尺寸
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        # 固定字體大小
        self.font_size = 16
        
        # 建立主要佈局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 建立 UI 元件
        self.create_widgets()
        
    def font_setup(self, font, font_size, font_weight, text_color_RGB):
        """設定文字樣式"""
        r, g, b = text_color_RGB
        font_set = f'font-family: "{font}"; font-size: {font_size}px; font-weight:{font_weight}; color:rgb({r}, {g}, {b});'
        return font_set
    
    def label_setup(self, text):
        """建立標籤"""
        label = QLabel(text, self)
        font_set = self.font_setup("微軟正黑體", self.font_size, 'bold', [0, 0, 0])
        label.setStyleSheet(font_set)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return label
    
    def entry_setup(self, prompt_text):
        """建立輸入框"""
        entry = QLineEdit(self)
        entry.setPlaceholderText(prompt_text)
        font_set = self.font_setup("微軟正黑體", self.font_size, 'bold', [0, 0, 0])
        entry.setStyleSheet(f'{font_set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px')
        entry.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return entry
    
    def combobox_setup(self):
        """建立下拉式選單"""
        combo_box = QComboBox(self)
        font_set = self.font_setup("微軟正黑體", self.font_size, 'bold', [0, 0, 0])
        combo_box.setStyleSheet(f'{font_set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px')
        combo_box.addItems(['請選擇性別', '男', '女', '其他'])
        combo_box.setCurrentIndex(0)
        return combo_box
    
    def create_grid_container(self):
        """建立放QGrid的容器和grid_layout"""
        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_container.setStyleSheet("border: 1px solid red;")
        return grid_container, grid_layout
    
    def setup_grid_layout(self, grid_layout):
        """設定QGridLayout"""
        column_ratio = [1, 2, 1, 2]  # Label Entry列的比例
        for i, ratio in enumerate(column_ratio):
            grid_layout.setColumnStretch(i, ratio)
        
        for j in range(8):
            grid_layout.setRowStretch(j, 1)
        
        # 固定邊界
        grid_layout.setContentsMargins(50, 0, 50, 0)
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(20)
    
    def create_widgets(self):
        """建立所有的UI元件"""
        text = ['編號 :', '性別 :', '拍攝日期 :', '年齡 :', '生日 :', '病史 :', '聯絡電話 :', '注意事項 :']
        
        # 建立容器和佈局
        self.grid_container, self.grid_layout = self.create_grid_container()
        self.main_layout.addWidget(self.grid_container)
        
        # 設定網格佈局
        self.setup_grid_layout(self.grid_layout)
        
        # 建立標題
        self.title = self.label_setup('個人資料')
        self.grid_layout.addWidget(self.title, 0, 0, 1, 4)
        self.grid_layout.setAlignment(self.title, Qt.AlignmentFlag.AlignCenter)
        
        # 儲存所有的輸入元件以便後續存取
        self.entries = {}
        self.labels = []
        
        # 建立標籤和輸入框
        label_positions = [
            (1, 0), (2, 0), (3, 0), (4, 0),  # 左邊欄位
            (1, 2), (2, 2), (3, 2), (4, 2)   # 右邊欄位
        ]
        
        entry_positions = [
            (1, 1), (2, 1), (3, 1), (4, 1),  # 左邊欄位
            (1, 3), (2, 3), (3, 3), (4, 3)   # 右邊欄位
        ]
        
        entry_keys = ['id', 'gender', 'shooting_date', 'age', 'birthday', 'medical_history', 'phone', 'notes']
        placeholder_texts = ['請輸入編號', '', '請輸入拍攝日期', '請輸入年齡', 
                           '請輸入生日', '請輸入病史', '請輸入聯絡電話', '請輸入注意事項']
        
        for i, (label_text, label_pos, entry_pos, key, placeholder) in enumerate(
            zip(text, label_positions, entry_positions, entry_keys, placeholder_texts)):
            
            # 建立標籤
            label = self.label_setup(label_text)
            self.labels.append(label)
            self.grid_layout.addWidget(label, *label_pos)
            
            # 建立對應的輸入元件
            if key == 'gender':
                entry_widget = self.combobox_setup()
            else:
                entry_widget = self.entry_setup(placeholder)
            
            self.entries[key] = entry_widget
            self.grid_layout.addWidget(entry_widget, *entry_pos)
    
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AD Sensor Application")
        self.resize(1200, 700)
        
        # Create main layout widget
        main_widget = QWidget()
        main_layout = QGridLayout(main_widget)
        self.setCentralWidget(main_widget)
        
        # Create image viewer (camera feed will be displayed here)
        self.image_viewer = ImageViewer()
        main_layout.addWidget(self.image_viewer, 0, 0, 1, 1)
        
        # Create tab widget for different operational panels
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget, 0, 1, 1, 1)
        
        # Create info panel as the first tab
        self.info_panel = InfoEntryPanel()
        self.tab_widget.addTab(self.info_panel, "個人資料")
        
        # Add additional tabs as needed
        # Example: Add a settings panel
        settings_panel = QWidget()
        settings_layout = QVBoxLayout(settings_panel)
        settings_layout.addWidget(QLabel("設定選項將在此處顯示"))
        self.tab_widget.addTab(settings_panel, "設定")
        
        # Example: Add an analysis panel
        analysis_panel = QWidget()
        analysis_layout = QVBoxLayout(analysis_panel)
        analysis_layout.addWidget(QLabel("分析結果將在此處顯示"))
        self.tab_widget.addTab(analysis_panel, "分析")
        
        # Set column stretch to give image viewer more space
        main_layout.setColumnStretch(0, 3)  # Image viewer gets more horizontal space
        main_layout.setColumnStretch(1, 2)  # Tab panel gets less horizontal space



def main():
    import cv2
    from PyQt6.QtWidgets import QTabWidget
    """主程式"""
    app = QApplication(sys.argv)
    
    # 建立 InfoEntryPanel 實例
    main_window = MainWindow()
    main_window.show()

    cam = cv2.VideoCapture(0)  # 使用第一個攝影機    
    def update_frame(cam):
        ret, frame = cam.read()
        if ret:
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            main_window.image_viewer.update_view(frame)


    sys.exit(app.exec())


if __name__ == "__main__":
    main()