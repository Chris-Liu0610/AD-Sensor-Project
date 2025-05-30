import cv2
import numpy as np
import pyrealsense2 as rs
import os
import time


class RealSenseCamera:
    def __init__(self, width=640, height=480, fps=30):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)
        self.config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
        self.start()

    def start(self):
        self.pipeline.start(self.config)
        sensor = self.pipeline.get_active_profile().get_device().query_sensors()[1]
        sensor.set_option(rs.option.enable_auto_exposure, False)
        sensor.set_option(rs.option.exposure, 100)
        sensor.set_option(rs.option.gain, 64)

    def stop(self):
        self.pipeline.stop()

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

        # 中心區域設定
        x_center = int(color_image.shape[1] / 2)
        y_center = int(color_image.shape[0] / 2)
        square_size = 80
        cv2.rectangle(color_image, 
                      (x_center - square_size, y_center - square_size), 
                      (x_center + square_size, y_center + square_size), 
                      (0, 255, 0), 2)

        have_face = False
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.03, minNeighbors=7, minSize=(100, 100))

        if len(faces) > 1:
            max_area = 0
            for (x, y, w, h) in faces:
                if w * h > max_area:
                    max_area = w * h
                    max_face = (x, y, w, h)
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

        #color_image = cv2.resize(color_image, (0, 0), fx=0.75, fy=0.75)
        return original_color_image, color_image, depth_image, have_face
    
    def get_frame(self):
        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                return None
            frame = np.asanyarray(color_frame.get_data())
            frame = cv2.transpose(frame)
            return frame
        except:
            return None



class CameraDevice:
    def __init__(self, camera_type="RealSense"):
        self.camera_types = ["RealSense"]
        self.camera_devices = [RealSenseCamera()]
        self.camera_type = camera_type
        self.camera = self.camera_devices[self.camera_types.index(camera_type)]
        self.camera.start()



    def start(self):
        self.camera.start()

    def stop(self):
        self.camera.stop()

    def get_frame(self):
        return self.camera.get_frame()

    def release(self):
        self.stop()


class VideoRecorder:
    def __init__(self, output_format="mp4", width=640, height=480, fps=30):
        self.output_format = output_format
        self.fps = fps
        self.writer = None
        self.is_recording = False
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.duration_count = 0
        self.frame_folder = "frames"
        os.makedirs(self.frame_folder, exist_ok=True)

    def set_config(self, width=640, height=480, fps=30, duration_seconds=5):
        self.width = width
        self.height = height
        self.fps = fps
        self.duration_frame_count = int(fps * duration_seconds)

    def start(self, filename="output.mp4"):
        print(f"Recording to {filename}...")
        if self.is_recording:
            raise RuntimeError("Recording is already in progress.")
        #接收第一幀並設定大小


        self.writer = cv2.VideoWriter(filename, self.fourcc, self.fps, (self.height, self.width))
        self.is_recording = True
        self.duration_count = 0
        self.frame_index = 1

    def stop(self):
        if not self.is_recording:
            raise RuntimeError("Recording is not in progress.")
        self.writer.release()
        self.is_recording = False

    def record_frame(self, frame=None):
        print(f"{self.is_recording=}")
        if not self.is_recording or frame is None:
            return
        if self.duration_count >= self.duration_frame_count:
            self.stop()
            return
        print("Recording frame...")
        self.writer.write(frame)
        # image_path = os.path.join(self.frame_folder, f"frame_{self.frame_index}.jpg")
        # cv2.imwrite(image_path, frame)
        self.frame_index += 1
        self.duration_count += 1




