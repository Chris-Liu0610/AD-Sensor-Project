import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from widget_helper import label_setup, entry_setup, date_setup, button_setup


class LEDWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LED檢視")
        self.setStyleSheet("background-color: rgb(248, 249, 250);")
        self.setFixedSize(800, 600)
        self.button_func = {}
        self.test_record = {}
        # self.LED_color = {'LED_color':['#FF0000', '#FF1500', '#FF2A00', '#FF3F00', '#FF5400', '#FF6A00', '#FF7F00'
        #                                , '#FF9400', '#FFAA00', '#FFBF00', '#FFD400', '#FFE900', '#FFFF00', '#E9FF00'
        #                                , '#D4FF00', '#BFFF00', '#AAFF00', '#94FF00', '#7FFF00', '#6AFF00', '#54FF00'
        #                                , '#3FFF00', '#2AFF00', '#15FF00', '#00FF00', '#00FF15', '#00FF2A']}
        self.ui()

    def ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # self.main_layout.setSpacing(10)

        #==== Create first grid layout ====#
        grid1_box = QtWidgets.QWidget()
        grid1_box.setStyleSheet("")
        grid1_box.setFixedHeight(40)
        grid1_layout = QtWidgets.QGridLayout(grid1_box)
        label_LED = label_setup("LED檢視", lambda: None)
        label_LED.setStyleSheet("font-size: 24px; font-weight: bold; color: rgb(0, 0, 0); border: 0px;")
        grid1_layout.addWidget(label_LED, 0, 0)
        grid1_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        #==== Finish ====#

        #===== Create second grid layout =====#
        grid2_box = QtWidgets.QWidget()
        grid2_box.setStyleSheet("border: 0px;")
        grid2_box.setFixedHeight(60)
        grid2_layout = QtWidgets.QGridLayout(grid2_box)
        
        label_LED_state = label_setup("LED狀態 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        label_LED_state.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        label_LED_state.setFixedWidth(100)
        grid2_layout.addWidget(label_LED_state, 0, 0)
        state_circle = label_setup("", lambda: None)
        state_circle.setFixedSize(30,30)
        state_circle.setStyleSheet("background-color: rgb(192, 192, 192); border-radius: 15px; border: 2px solid rgb(0, 0, 0);") # 這邊要設置顏色，當LED開始作用亮綠燈，當退出LED亮白色
        self.button_func['state_circle'] = state_circle
        grid2_layout.addWidget(state_circle, 0, 1, 1, 3)
        
        #===== Create third grid layout =====#
        grid3_box = QtWidgets.QWidget()
        grid3_box.setStyleSheet("border: 0px solid rgb(0, 0, 0);")
        grid3_layout = QtWidgets.QGridLayout(grid3_box)

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
        combine_layout2_layout3_box = QtWidgets.QWidget()
        combine_layout2_layout3_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border: 2px solid rgb(0, 0, 0);")
        combine_layout2_layout3 = QtWidgets.QVBoxLayout(combine_layout2_layout3_box)
        combine_layout2_layout3.addWidget(grid2_box)
        combine_layout2_layout3.addWidget(grid3_box)
        #==== Finish ====#
        
        #==== Create fourth grid layout ====#
        # grid4_box = QtWidgets.QWidget()
        # grid4_box.setStyleSheet("")
        # grid4_box.setFixedHeight(40)
        # grid4_layout = QtWidgets.QGridLayout(grid4_box)

        # label_LED_show = label_setup("LED顯示 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        # label_LED_show.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        # label_LED_show.setFixedWidth(100)
        # grid4_layout.addWidget(label_LED_show, 0, 0, 1, 4)
        #==== Finish ====#

        # #==== Create fifth grid layout ====#
        # grid5_box = QtWidgets.QWidget()
        # grid5_box.setStyleSheet("border: 2px solid rgb(0, 0, 0);")
        # grid5_layout = QtWidgets.QGridLayout(grid5_box)
        
        # LED_number = 27
        # column = 9
        # for i in range(LED_number):
        #     row = i // column
        #     col = i % column
        #     show_circle = label_setup("", lambda: None)
        #     show_circle.setFixedSize(30, 30)
        #     show_circle.setStyleSheet("background-color: rgb(192, 192, 192); border-radius: 15px; border: 2px solid rgb(0, 0, 0);")
        #     grid5_layout.addWidget(show_circle, row, col)  # Start from row 1 to leave space for the label
        #     self.button_func[f'show_circle_{i}'] = show_circle
        # #==== Finish ====#
        
        #==== Create combine fourth and fifth grid layout ====#
        # combine_layout4_layout5_box = QtWidgets.QWidget()
        # combine_layout4_layout5_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px;")
        # combine_layout4_layout5 = QtWidgets.QVBoxLayout(combine_layout4_layout5_box)
        # combine_layout4_layout5.addWidget(grid4_box)
        # combine_layout4_layout5.addWidget(grid5_box)
        #==== Finish ====#

        #==== Create sixth grid layout ====#
        grid6_box = QtWidgets.QWidget()
        grid6_box.setStyleSheet("border: 0px;")
        grid6_box.setFixedHeight(40)
        grid6_layout = QtWidgets.QGridLayout(grid6_box)
        label_test_record = label_setup("測試紀錄 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        grid6_layout.addWidget(label_test_record, 0, 0, 1, 4)
        #==== Finish ====#

        #==== Create seventh grid layout ====#
        grid7_box = QtWidgets.QWidget()
        grid7_box.setStyleSheet("border: 0px solid rgb(0, 0, 0);")
        grid7_layout = QtWidgets.QGridLayout(grid7_box)
        self.entry_test_record = QtWidgets.QTextEdit(self)
        self.entry_test_record.setReadOnly(True)
        self.entry_test_record.setStyleSheet("background-color: rgb(255, 255, 255); font-size: 14px; font-family: 微軟正黑體; font-weight: bold; border: 0px; border-radius: 10px; color: rgb(0, 0, 0);")
        self.test_record['record'] = self.entry_test_record
        grid7_layout.addWidget(self.entry_test_record, 0, 0, 1, 4)
        #==== Finish ====#
        
        #==== Create combine sixth and seventh grid layout ====#
        combine_layout6_layout7_box = QtWidgets.QWidget()
        combine_layout6_layout7_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border: 2px solid rgb(0, 0, 0);")
        combine_layout6_layout7 = QtWidgets.QVBoxLayout(combine_layout6_layout7_box)
        combine_layout6_layout7.addWidget(grid6_box)
        combine_layout6_layout7.addWidget(grid7_box)
        #==== Finish ====#

        #==== Create eighth grid layout ====#
        grid8_box = QtWidgets.QWidget()
        grid8_box.setStyleSheet("")
        grid8_layout = QtWidgets.QGridLayout(grid8_box)

        button_back = button_setup("上一步", lambda: print("上一步按鈕被點擊"))
        grid8_layout.addWidget(button_back, 0, 0, 1, 1)
        self.button_func['button_back'] = button_back

        grid8_layout.setSpacing(400)

        button_next = button_setup("下一步", lambda: print("下一步按鈕被點擊"))
        grid8_layout.addWidget(button_next, 0, 1, 1, 1)
        self.button_func['button_next'] = button_next
        
        

        #==== Finally, add the grid layout to the main layout ====#
        self.main_layout.addWidget(grid1_box)
        self.main_layout.addWidget(combine_layout2_layout3_box)
        # self.main_layout.addWidget(grid4_box)
        self.main_layout.addWidget(combine_layout6_layout7_box)
        self.main_layout.addWidget(grid8_box)
        #===== Finish =====#



    


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LEDWindow()
    window.show()
    sys.exit(app.exec())