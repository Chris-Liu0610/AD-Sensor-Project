from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QImage, QPixmap
import sys, cv2, numpy as np
import pyrealsense2 as rs
from Camera_GUI import CameraWindow
from LED import ArduinoController
from Personal_GUI import PersonalWindow
import os
import time

from threading import Thread
from queue import Queue
from multiprocessing import Process, Queue as MPQueue


class TimeTesting:
    def __init__(self):
        self.start_time = time.time()

    def start(self):
        self.start_time = time.time()

    def print_elapsed_time(self):
        elapsed_time = time.time() - self.start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")

    def reset(self):
        self.start_time = time.time()

# Evaluate the record frame rate is correct
class FPSMeter:
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 2.0:
            self.start_time = time.time()
            self.frame_count = 0

    def print_fps(self):
        elapsed_time = time.time() - self.start_time
        fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
        print(f"FPS: {fps:.2f}", end="\r", flush=True)

    def fps(self):
        elapsed_time = time.time() - self.start_time
        fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
        return fps if self.frame_count > 0 else 0


class CameraPresenter:
    def __init__(self, arduino_controller=None):
        super().__init__()
        self.window_camera = CameraWindow()
        self.window_personal = PersonalWindow()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        if arduino_controller is None:
            raise ValueError("ArduinoController instance is required.")
        self.led_controller : ArduinoController = arduino_controller
        
        # RealSense 設定
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.pipeline.start(config)

        self.recorderType = False # 設定是否處於錄影狀態，預設 False
        self.ocv = True
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v') # 設定存檔影片格式
        self.output = None
        self.scale = 1

        self.ID = ""

        # 按鈕事件
        self.window_camera.record_button.clicked.connect(self.recordVideo)
        self.window_camera.save_button.clicked.connect(self.save_path)

        self.frame_rate = FPSMeter()  # 計算 FPS
        self.time_testing = TimeTesting()  # 計算時間

        self.buffer = Queue(maxsize=360)  # 設定緩衝區大小
        self.workers = [
            Thread(target=self._show_frame, args=(self.face_cascade,), daemon=True) for _ in range(2)
        ]
        self.workers += [
            Thread(target=self._update_frame, daemon=True)
        ]

        self.mp_queue = MPQueue(maxsize=360)  # 設定多進程緩衝區大小
        self.mp_processes = [
            Process(target=self.show_frame, args=(self.face_cascade, self.mp_queue), daemon=True) for _ in range(4)
        ]

        # Start the worker threads
        for worker in self.workers:
            worker.start()

        # 定時更新畫面
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(33)


    def recordVideo(self):

        if not self.recorderType:

            self.output_path = self.window_camera.entry_folder_entry.text() # 取得路徑

            if not self.output_path:
                print("請選擇儲存路徑")
                return

            video_path = os.path.join(self.output_path, f'{self.ID}.mp4')
            print(video_path)
            self.output = cv2.VideoWriter(video_path, self.fourcc, 30.0, (480, 640)) # 設定儲存影片的檔案
            self.time_testing.start()  # 開始計時
            self.recorderType = True
            self.led_controller.start_led()
            self.window_camera.record_button.setText("錄影中，點擊停止錄影")
            self.led_controller.flash_led_3_times()
            QtCore.QTimer.singleShot(3000, lambda: self.led_controller.cycle_flash())
        else:
            self.time_testing.print_elapsed_time()
            self.output.release()
            self.recorderType = False
            self.led_controller.exit_led()
            self.window_camera.record_button.setText("點擊開始錄影")

    def update_fps(self): 
        self.window_camera.fps_label.setText(f"FPS: {self.frame_rate.fps():.2f}")

    def _show_frame(self, face_cascade):
        while True:
            try:
                self.mp_queue.put(self.show_frame(face_cascade), timeout=0.1)
            except Exception as e:
                print(f"Buffer is full: {e}")
                continue
            time.sleep(0.01)  # 控制緩衝區的更新頻率


    def _update_frame(self):
        while True:
            self.update_frame()
            time.sleep(0.01)

    def update_frame(self):

        # color_orig, color_img, depth_img, have_face = self.show_frame(self.face_cascade)
        # color_orig, color_img, depth_img, have_face = self.get_frame()
        if not self.mp_queue.empty():
            color_orig, color_img, _, _ = self.mp_queue.get(timeout=0.2)
        else:
            color_orig, color_img, _, _ = None, None, None, False

        if color_img is None:
            return

        if self.recorderType and self.output is not None:
            self.output.write(color_orig)

        self.frame_rate.update()  # 更新 FPS 計算
        # self.frame_rate.print_fps()  # 印出 FPS
        self.window_camera.fps_label.setText(f"FPS: {self.frame_rate.fps():.2f}")

        # 顯示影像
        rgb_frame = cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.window_camera.camera_label.setPixmap(QPixmap.fromImage(qt_img))

    def show_frame(self, face_cascade):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            return None, None, None, False

        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.transpose(color_image)
        original_color_image = color_image.copy()
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_image = cv2.transpose(depth_image)

       
        x_center = int(color_image.shape[1] / 2)
        y_center = int(color_image.shape[0] / 2)
        square_size = 80
        cv2.rectangle(color_image,
                    (x_center - square_size, y_center - square_size),
                    (x_center + square_size, y_center + square_size),
                    (0, 255, 0), 2)

        have_face = False

        if not self.recorderType:

            gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.03, minNeighbors=7, minSize=(100, 100))

            if len(faces) > 1:
                max_face = max(faces, key=lambda f: f[2] * f[3])
                faces = [max_face]

            for (x, y, w, h) in faces:
                x_center_face, y_center_face = int(x + w / 2), int(y + h / 2)
                cv2.circle(color_image, (x_center_face, y_center_face), 5, (0, 0, 255), 2)

                depth_roi = depth_image[y:y + h, x:x + w] / 1000.0
                valid_mask = (depth_roi > 0.1) & (depth_roi < 1.0)
                valid_distances = depth_roi[valid_mask]
                ave_distance = np.mean(valid_distances) if valid_distances.size > 0 else 0

                color = (0, 255, 0)
                if 0.35 <= ave_distance <= 0.5:
                    if x_center - square_size < x_center_face < x_center + square_size and y_center - square_size < y_center_face < y_center + square_size:
                        color = (0, 0, 255)
                        have_face = True

                text = f"Distance: {ave_distance:.2f} m"
                cv2.rectangle(color_image, (x, y), (x + w, y + h), color, 2)
                cv2.putText(color_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            

        return original_color_image, color_image, depth_image, have_face
    
    def save_path(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory()
        if folder_path:
            self.window_camera.entry_folder_entry.setText(folder_path)

    def patient_ID(self, patient_ID):
        self.ID = patient_ID

    def closeEvent(self, event):
        QtCore.QTimer.singleShot(0, self.cleanup_resources)
        event.accept()

    def cleanup_resources(self):
        self.ocv = False
        if self.led_controller.is_running:
            self.led_controller.exit_led()
            self.led_controller.close()

        if self.timer.isActive():
            self.timer.stop()
        if self.output and self.output.isOpened():
            self.output.release()
            self.output = None

        self.pipeline.stop()

    def connect_back_second_button(self, back_function):
        self.window_camera.back_button.clicked.connect(back_function)


    def show(self):
        self.window_camera.closeEvent = self.closeEvent
        self.window_camera.show()

    def hide(self):
        self.window_camera.hide()
        self.window_camera.closeEvent = self.closeEvent

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    arduino_controller = ArduinoController()
    widget = CameraPresenter(arduino_controller)
    widget.show()
    sys.exit(app.exec())