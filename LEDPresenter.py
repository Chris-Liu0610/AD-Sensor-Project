from LED import ArduinoController
from LED_GUI import LEDWindow
from PyQt6 import QtWidgets
import sys


class LEDPresenter:
    def __init__(self, arduino_controller=None):
        self.view = LEDWindow()
        if arduino_controller is None:
            raise ValueError("ArduinoController instance is required.")
        self.led_controller : ArduinoController = arduino_controller

        self.view.LED_start_button.clicked.connect(self.connect_LED_work)
        self.view.LED_exit_button.clicked.connect(self.connect_LED_exit)
        self.view.LED_flicker_3times_button.clicked.connect(self.connect_LED_flicker_3times)
        self.view.LED_cycle_flicker_button.clicked.connect(self.connect_LED_cycle_flicker)
        self.view.LED_stop_button.clicked.connect(self.connect_LED_stop)

        # self.timer = QtCore.QTimer(self.view)
        # self.timer.setInterval(500)
        # self.timer.timeout.connect(self.update_LED_three_times)

    def connect_LED_work(self):
        self.view.button_func['state_circle'].setFixedSize(30,30)
        self.view.button_func['state_circle'].setStyleSheet("background-color: green; border-radius: 15px; border: 2px solid rgb(0, 0, 0);")
        self.led_controller.start_led()
        self.view.test_record['record'].append("LED開始運作")
        

    def connect_LED_exit(self):
        self.view.button_func['state_circle'].setFixedSize(30,30)
        self.view.button_func['state_circle'].setStyleSheet("background-color: rgb(192, 192, 192); border-radius: 15px; border: 2px solid rgb(0, 0, 0);")
        self.led_controller.exit_led()
        self.view.test_record['record'].append("LED退出")

    def connect_LED_flicker_3times(self):
        
        # self.count = 0
        # self.view.LED_flicker_3times_button.setEnabled(False)
        # self.update_LED_three_times()
        # self.timer.start()
        self.led_controller.flash_led_3_times()
        self.view.test_record['record'].append("LED閃爍三次")
    
    def connect_LED_cycle_flicker(self):
        # self.view.button_func['state_circle'].setFixedSize(30,30)
        # self.view.button_func['show_circle_0'].setStyleSheet("background-color: white; border-radius: 15px; border: 2px solid rgb(0, 0, 0);")
        self.led_controller.cycle_flash()
        self.view.test_record['record'].append("LED循環閃爍")

    def connect_LED_stop(self):
        # self.view.button_func['state_circle'].setFixedSize(30,30)
        # self.view.button_func['show_circle_0'].setStyleSheet("background-color: white; border-radius: 15px; border: 2px solid rgb(0, 0, 0);")
        self.led_controller.stop_led()
        self.view.test_record['record'].append("LED停止")

    def connect_next_third_button(self, next_function):
        self.view.button_func['button_next'].clicked.connect(next_function)

    def connect_back_first_button(self, back_function):
        self.view.button_func['button_back'].clicked.connect(back_function)

    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    arduino_controller = ArduinoController()
    presenter = LEDPresenter(arduino_controller)
    presenter.show()
    sys.exit(app.exec())