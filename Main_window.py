# from test import SecondWindow, ThirdWindow, FourthWindow, MainWindow
from Personal_GUI import PersonalWindow
from LEDPresenter import LEDPresenter
from CameraPresenter import CameraPresneter
from PyQt6 import QtWidgets
from LED import ArduinoController
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = PersonalWindow()
        self.window1.connect_next_second_button(self.show_second_window)
        arduino_controller = ArduinoController()
        self.window2 = LEDPresenter(arduino_controller)
        self.window2.connect_next_third_button(self.show_third_window)
        self.window2.connect_back_first_button(self.back_to_first_window)
        self.window3 = CameraPresneter(arduino_controller)
        

    def show(self): # 程式開始時顯示第一個視窗
        self.window1.show()
    
    def show_second_window(self):
        self.window1.hide()
        self.window2.show()
    
    def show_third_window(self):
        self.window2.hide()
        self.window3.show()

    def back_to_first_window(self):
        self.window2.hide()
        self.window1.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())