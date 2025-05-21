import cv2
import numpy as np
import pyrealsense2 as rs



class WebcamCamera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.capture = cv2.VideoCapture(camera_index)

    def start(self):
        self.capture.open(self.camera_index)

    def stop(self):
        self.capture.release()

    def get_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return None
        return frame


class RealSenseCamera:
    def __init__(self, width=640, height=480, fps=30):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)

    def reset(self, width=640, height=480, fps=30):
        self.stop()
        self.__init__(width, height, fps)

    def start(self):
        self.pipeline.start(self.config)

    def stop(self):
        self.pipeline.stop()

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            return None
        frame = np.asanyarray(color_frame.get_data())
        return frame


class CameraDevice:
    def __init__(self, camera_type="Webcam"):
        self.camera_types = ["Webcam", "RealSense"]        
        self.camera_devices = [WebcamCamera(), RealSenseCamera()]
        self.camera_type = camera_type
        self.camera = self.camera_devices[self.camera_types.index(camera_type)]
        self.camera.start()

    def switch_camera(self, camera_type):
        if camera_type not in self.camera_types:
            raise ValueError(f"Invalid camera type: {camera_type}")
        self.camera.stop()
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
        self.camera.release()


class VideoRecorder:
    def __init__(self, width=640, height=480, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.writer = None
        self.is_recording = False
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.duration_count = 0

    def set_config(self, filename, width=640, height=480, fps=30, duration=None):
        self.filename = filename
        self.fps = fps
        self.width = width
        self.height = height
        self.duration = duration * fps if duration else None

    def start(self):
        self.writer = cv2.VideoWriter(
            self.filename, self.fourcc, self.fps, (self.width, self.height)
        )
        self.is_recording = True
        self.duration_count = 0

    def stop(self):
        self.writer.release()
        self.is_recording = False

    def record_frame(self, frame):
        if frame is None:
            raise ValueError("Frame is None.")
        if self.duration is None or self.duration_count >= self.duration:
            self.stop()
            return
        self.writer.write(frame)
        self.duration_count += 1

    

if __name__ == "__main__":
    camera = CameraDevice(camera_type="RealSense")  # Change to "Webcam" for webcam
    video_recorder = VideoRecorder()
    video_recorder.set_config(filename="output.mp4", width=640, height=480, fps=30, duration=3)  # Set the desired configuration
    print(video_recorder.is_recording)
    camera_types = ["Webcam", "RealSense"] 
    cam_idx = 0
    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        # Display the frame
        cv2.imshow("Webcam", frame)
        if video_recorder.is_recording:
            # Record the frame
            video_recorder.record_frame(frame)
            
        key = cv2.waitKey(1) & 0xFF
        # Break the loop on 'q' key press
        if key == ord('q'):
            break
        if key == ord('c'):
            camera.switch_camera(camera_types[cam_idx])
            cam_idx = (cam_idx + 1) % len(camera_types)
        if key == ord('s'):
            video_recorder.start()

    camera.stop()
    cv2.destroyAllWindows()