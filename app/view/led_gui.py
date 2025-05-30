from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QTextEdit,
    QVBoxLayout,
    QWidget
)

from utils.widget_helper import label_setup, button_setup


class LEDWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LED檢視")
        self.setStyleSheet("background-color: rgb(248, 249, 250);")
        self.setFixedSize(800, 600)
        self.button_func = {}
        self.test_record = {}
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        # self.main_layout.setSpacing(10)

        #==== Create first grid layout ====#
        grid1_box = QWidget()
        grid1_box.setStyleSheet("")
        grid1_box.setFixedHeight(40)
        grid1_layout = QGridLayout(grid1_box)
        label_LED = label_setup("LED檢視", lambda: None)
        label_LED.setStyleSheet("font-size: 24px; font-weight: bold; color: rgb(0, 0, 0); border: 0px;")
        grid1_layout.addWidget(label_LED, 0, 0)
        grid1_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #==== Finish ====#

        #===== Create second grid layout =====#
        grid2_box = QWidget()
        grid2_box.setStyleSheet("border: 0px;")
        grid2_box.setFixedHeight(60)
        grid2_layout = QGridLayout(grid2_box)
        
        label_LED_state = label_setup("LED狀態 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        label_LED_state.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        label_LED_state.setFixedWidth(100)
        grid2_layout.addWidget(label_LED_state, 0, 0)
        state_circle = label_setup("", lambda: None)
        state_circle.setFixedSize(30,30)
        state_circle.setStyleSheet("background-color: rgb(192, 192, 192); border-radius: 15px; border: 2px solid rgb(0, 0, 0);") # 這邊要設置顏色，當LED開始作用亮綠燈，當退出LED亮白色
        self.button_func['state_circle'] = state_circle
        grid2_layout.addWidget(state_circle, 0, 1, 1, 3)
        
        #===== Create third grid layout =====#
        grid3_box = QWidget()
        grid3_box.setStyleSheet("border: 0px solid rgb(0, 0, 0);")
        grid3_layout = QGridLayout(grid3_box)

        self.LED_start_button = button_setup("LED開始運作", lambda: None)
        grid3_layout.addWidget(self.LED_start_button, 0, 0, 1, 2)

        self.LED_exit_button = button_setup("LED退出", lambda: None)
        grid3_layout.addWidget(self.LED_exit_button, 0, 2, 1, 2)

        self.LED_flicker_3times_button = button_setup("LED閃爍三次", lambda: None)
        grid3_layout.addWidget(self.LED_flicker_3times_button, 1, 0, 1, 4)

        self.LED_cycle_flicker_button = button_setup("LED循環閃爍", lambda: None)
        grid3_layout.addWidget(self.LED_cycle_flicker_button, 2, 0, 1, 4)

        self.LED_stop_button = button_setup("LED停止", lambda: None)
        grid3_layout.addWidget(self.LED_stop_button, 3, 0, 1, 4)
        #==== Finish ====#
        
        #===== Create combine second and third grid layout =====#
        combine_layout2_layout3_box = QWidget()
        combine_layout2_layout3_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border: 2px solid rgb(0, 0, 0);")
        combine_layout2_layout3 = QVBoxLayout(combine_layout2_layout3_box)
        combine_layout2_layout3.addWidget(grid2_box)
        combine_layout2_layout3.addWidget(grid3_box)
        #==== Finish ====#
        
        #==== Create sixth grid layout ====#
        grid6_box = QWidget()
        grid6_box.setStyleSheet("border: 0px;")
        grid6_box.setFixedHeight(40)
        grid6_layout = QGridLayout(grid6_box)
        label_test_record = label_setup("測試紀錄 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        grid6_layout.addWidget(label_test_record, 0, 0, 1, 4)
        #==== Finish ====#

        #==== Create seventh grid layout ====#
        grid7_box = QWidget()
        grid7_box.setStyleSheet("border: 0px solid rgb(0, 0, 0);")
        grid7_layout = QGridLayout(grid7_box)
        self.entry_test_record = QTextEdit(self)
        self.entry_test_record.setReadOnly(True)
        self.entry_test_record.setStyleSheet("background-color: rgb(255, 255, 255); font-size: 14px; font-family: 微軟正黑體; font-weight: bold; border: 0px; border-radius: 10px; color: rgb(0, 0, 0);")
        self.test_record['record'] = self.entry_test_record
        grid7_layout.addWidget(self.entry_test_record, 0, 0, 1, 4)
        #==== Finish ====#
        
        #==== Create combine sixth and seventh grid layout ====#
        combine_layout6_layout7_box = QWidget()
        combine_layout6_layout7_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border: 2px solid rgb(0, 0, 0);")
        combine_layout6_layout7 = QVBoxLayout(combine_layout6_layout7_box)
        combine_layout6_layout7.addWidget(grid6_box)
        combine_layout6_layout7.addWidget(grid7_box)
        #==== Finish ====#

        #==== Create eighth grid layout ====#
        grid8_box = QWidget()
        grid8_box.setStyleSheet("")
        grid8_layout = QGridLayout(grid8_box)

        button_back = button_setup("上一步", lambda: None)
        grid8_layout.addWidget(button_back, 0, 0, 1, 1)
        self.button_func['button_back'] = button_back

        grid8_layout.setSpacing(400)

        button_next = button_setup("下一步", lambda: None)
        grid8_layout.addWidget(button_next, 0, 1, 1, 1)
        self.button_func['button_next'] = button_next
        
        

        #==== Finally, add the grid layout to the main layout ====#
        self.main_layout.addWidget(grid1_box)
        self.main_layout.addWidget(combine_layout2_layout3_box)
        # self.main_layout.addWidget(grid4_box)
        self.main_layout.addWidget(combine_layout6_layout7_box)
        self.main_layout.addWidget(grid8_box)
        #===== Finish =====#

