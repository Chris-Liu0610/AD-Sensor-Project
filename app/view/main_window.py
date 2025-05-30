import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from app.view.personal_gui import PersonalWindow
from app.presenter.led_presenter import LEDPresenter
from app.presenter.camera_presenter import CameraPresenter
from PyQt6 import QtWidgets
from app.model.led import ArduinoController


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = PersonalWindow()
        self.window1.connect_next_second_button(self.show_second_window)
        arduino_controller = ArduinoController()
        self.window2 = LEDPresenter(arduino_controller)
        self.window2.connect_next_third_button(self.show_third_window)
        self.window2.connect_back_first_button(self.back_to_first_window)
        self.window3 = CameraPresenter(arduino_controller)
        self.window3.connect_back_second_button(self.back_to_second_window)
        

    def show(self): # 程式開始時顯示第一個視窗
        self.window1.show()
    
    def show_second_window(self):

        entry_ID = self.window1.widgets.get("entry_ID")
        self.patient_ID = entry_ID.text()
        
        
        self.window1.hide()
        self.window2.show()

    
    def show_third_window(self):

        self.window3.patient_ID(self.patient_ID) # 傳入CameraPresenter的ID

        self.window2.hide()
        self.window3.show()

    def back_to_first_window(self):
        self.window2.hide()
        self.window1.show()

    def back_to_second_window(self):
        self.window3.hide()
        self.window2.show()

