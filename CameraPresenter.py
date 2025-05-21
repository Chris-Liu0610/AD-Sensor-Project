from Camera_GUI import CameraWindow
from LED import ArduinoController
from PyQt6 import QtWidgets, QtCore, QtGui
from camera_device import CameraApp, RealSenseCamera, VideoRecorder
import sys
import time


class CameraPresneter:
    def __init__(self, arduino_controller=None):
        self.camera_window = CameraWindow()
        # self.camera_device = CameraApp()
        self.camera_device = RealSenseCamera()
        self.video_recorder = VideoRecorder()
        self.video_recorder.set_config(duration_seconds=5)
        if arduino_controller is None:
            raise ValueError("ArduinoController instance is required.")
        self.arduino : ArduinoController = arduino_controller

        self.camera_window.record_button.clicked.connect(self.start_recording)
        self.camera_window.stop_button.clicked.connect(self.stop_recording)

        self.frame_timer = QtCore.QTimer(self.camera_window)
        self.frame_timer.timeout.connect(self.update_frame)
        self.frame_timer.start(33)


    def update_frame(self):
        frame = self.camera_device.get_frame()
        if frame is not None:
            self.video_recorder.record_frame(frame)
            q_img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format.Format_BGR888)
            q_pixmap = QtGui.QPixmap.fromImage(q_img)
            self.camera_window.camera_label.setPixmap(q_pixmap)
        else:
            print("No frame received.")

    def start_recording(self):
        self.arduino.start_led()
        self.arduino.flash_led_3_times()
        time.sleep(2.5)
        self.arduino.cycle_flash()
        # self.camera_device.run()
        self.video_recorder.start()

        

    def stop_recording(self):
        # self.arduino.stop_led()
        # self.arduino.exit_led()
       pass

    def show(self):
        self.camera_window.show()

class EmptyController:
    def __init__(self):
        pass

    def start_led(self):
        pass

    def start_recording(self):
        pass

    def flash_led_3_times(self):
        pass

    def cycle_flash(self):
        pass

    def stop_recording(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # arduino_controller = ArduinoController()
    arduino_controller = EmptyController()
    controller = CameraPresneter(arduino_controller)
    controller.camera_window.show()
    sys.exit(app.exec())
