import cv2
import numpy as np
import mediapipe as mp
import math
import matplotlib.pyplot as plt
import pandas as pd

from queue import Queue

from scipy.spatial.transform import Rotation as R
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class FacePoseDetector:
    def __init__(self):
        """初始化人臉姿態檢測器"""
        # 初始化 MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        # 初始化繪圖工具
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # 相機內參（假設值，實際應該通過相機標定獲得）
        self.camera_matrix = None
        self.dist_coeffs = np.zeros((4, 1))
        
        # 定義用於姿態估計的關鍵點索引
        self.pose_landmarks_indices = {
            'nose_tip': 4,          # 鼻尖
            'chin': 152,            # 下巴
            'left_eye_corner': 33,  # 左眼角
            'right_eye_corner': 263, # 右眼角
            'left_mouth_corner': 61, # 左嘴角
            'right_mouth_corner': 291, # 右嘴角
            'forehead': 10          # 額頭中心
        }
        
    def setup_camera_matrix(self):
        """設置相機矩陣（如果沒有標定數據，使用估計值）"""
        if self.camera_matrix is None:
            # 估計焦距
            self.camera_matrix = np.array([
                [385.73846, 0, 324.16235],
                [0, 385.73846, 241.51932],
                [0, 0, 1]
            ], dtype=np.float32)
    
    def get_face_3d_model(self, tilt_x_degrees, tilt_y_degrees, tilt_z_degrees):
        """獲取標準人臉3D模型的關鍵點(單位:cm)"""
        #基於平均人臉尺寸的3D模型點
        face_3d_model = {
            'nose_tip': [0.0, 0.0, 0.0],
            'chin': [0.0, -6.0, 3.0],
            'left_eye_corner': [3.5, 3.5, 3.0],
            'right_eye_corner': [-3.5, 3.5, 3.0],
            'left_mouth_corner': [2.5, -3.5, 2.0],
            'right_mouth_corner': [-2.5, -3.5, 2.0],
            'forehead': [0.0, 6.0, 3.0]
        }

        theta_x = math.radians(tilt_x_degrees)
        theta_y = math.radians(tilt_y_degrees)
        theta_z = math.radians(tilt_z_degrees)
        

        R_x = np.array([
                [1, 0, 0],
                [0, math.cos(theta_x), -math.sin(theta_x)],
                [0, math.sin(theta_x),  math.cos(theta_x)]
            ], dtype=np.float32)
        
        R_y = np.array([
                [math.cos(theta_y), 0, math.sin(theta_y)],
                [0, 1, 0],
                [-math.sin(theta_y), 0, math.cos(theta_y)]
            ], dtype=np.float32)
        
        R_z = np.array([
                [math.cos(theta_z), -math.sin(theta_z), 0],
                [math.sin(theta_z),  math.cos(theta_z), 0],
                [0, 0, 1]
            ], dtype=np.float32)
        
        R = R_x @ R_y @ R_z
        # 轉換為numpy數組
        points_3d = []
        for key in self.pose_landmarks_indices.keys():
            pt = np.array(face_3d_model[key], dtype=np.float32)
            # pt = points_3d.append(face_3d_model[key])
            rotated_pt = R @ pt
            # print(rotated_pt)
            points_3d.append(rotated_pt)
        
        return np.array(points_3d, dtype=np.float32)
    
    def detect_face_pose(self, image):
        """檢測人臉姿態"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)
        
        if not results.multi_face_landmarks:
            return None, None, None
        
        # 獲取圖像尺寸
        self.setup_camera_matrix()
        
        # 獲取第一張臉的關鍵點
        face_landmarks = results.multi_face_landmarks[0]
        
        # 提取用於姿態估計的2D點
        h, w, _ = image.shape
        image_points = []
        for key, idx in self.pose_landmarks_indices.items():
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            image_points.append([x, y])
        
        image_points = np.array(image_points, dtype=np.float32)
        
        # 獲取對應的3D模型點
        object_points = self.get_face_3d_model(tilt_x_degrees = 0, tilt_y_degrees = 0, tilt_z_degrees = 0)
        
        # 使用PnP算法求解姿態
        success, rvec, tvec = cv2.solvePnP(object_points, image_points, self.camera_matrix, self.dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
        # print(rvec)

        if not success:
            return None, None, None
        
        
        return rvec, tvec, image_points
    
    def get_euler_angles(self, rvec):

        rvec = rvec.flatten()
        r = R.from_rotvec(rvec)
        angle = r.as_euler('xyz', degrees=True)

        print(f"\r{angle}", end='', flush=True)
    
        return angle
    

    def annotate_image(self, image, rvec):
        """在圖像上添加完整的姿態標註"""
        frame = image.copy()
        

        # 計算並顯示歐拉角
        angle = self.get_euler_angles(rvec)
        
        # 在圖像上顯示角度信息
        info_text = [f"Pitch: {angle[0]:.1f} degree", f"Yaw: {angle[1]:.1f} degree", f"Roll: {angle[2]:.1f} degree"]
        
        # 背景框
        cv2.rectangle(frame, (5, 5), (250, 110), (248, 249, 250), -1)
        
        for i, text in enumerate(info_text):
            color = [(51, 51, 255), (51, 255, 51), (255, 51, 51)][i]  # 對應的顏色
            cv2.putText(frame, text, (15, 35 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
        
        return frame



# ============================================================
#  MatplotlibWavePlot - Real-time 3x1 wave plotting
# ============================================================
class MatplotlibWavePlot:
    """Real-time plotting of three waveforms in a vertically stacked layout."""
    
    def __init__(self, max_points=1500):
        """
        Initialize the wave plot.
        
        Args:
            max_points: Maximum number of points to display (default: 1200)
        """
        # Set up figure and subplots
        self.fig = Figure(figsize=(8, 6))
        self.axes = [self.fig.add_subplot(3, 1, i+1) for i in range(3)]
        self.canvas = FigureCanvas(self.fig)
        
        # Configure each subplot
        titles = ['Pitch', 'Yaw', 'Roll']
        colors = ['blue', 'green', 'red']
        
        # Initialize empty lines
        self.lines = []
        
        for i, ax in enumerate(self.axes):
            line, = ax.plot([], [], color=colors[i], lw=1)
            self.lines.append(line)
            ax.set_title(f"{titles[i]} vs Time")
            ax.set_ylabel(f"{titles[i]} (deg)")
            ax.set_xlim(0, max_points // 150)  # Initial 30 seconds window
            ax.set_ylim(-20, 20)  # Reasonable range for head angles
            ax.grid(True)
            
        # Set common x label for bottom subplot
        self.axes[-1].set_xlabel("Time (s)")
        
        # Tight layout for better spacing
        self.fig.tight_layout()
        
        # Store references to specific lines for easy access
        self.pitch_line = self.lines[0]
        self.yaw_line = self.lines[1]
        self.roll_line = self.lines[2]

        self.time_data = np.arange(0, max_points) / 30  # Assuming 30 FPS, adjust as needed
        
    def update_plot(self, pitch_data, yaw_data, roll_data, time_data=None):

        # Make sure data arrays have the same length
        data_length = len(pitch_data)
        x_data = time_data if time_data is not None else self.time_data[:data_length]
        
        # Update each line with new data
        self.pitch_line.set_data(x_data, pitch_data)
        self.yaw_line.set_data(x_data, yaw_data)
        self.roll_line.set_data(x_data, roll_data)

        # for ax in self.axes:
        #     ax.set_xlim(0, pitch_data.size / 30)  # Update x-axis limits based on data length
        
        # Redraw the canvas
        self.canvas.draw()

    def clear(self):
        """Clear all plot lines."""
        for line in self.lines:
            line.set_data([], [])
        self.canvas.draw()
        
    def update_xlim(self, new_limit):
        """Update the x-axis limits for all subplots."""
        for ax in self.axes:
            ax.set_xlim(0, new_limit)

# ============================================================
#  PoseTracker －－同時追蹤 Pitch 與 Yaw
# ============================================================
class PoseTracker:

    def __init__(self, video_path, video_output_path):
        
        self.video_path = video_path
        self.video_output_path = video_output_path

        # ---------- 偵測器與影片 ----------
        self.detector = FacePoseDetector()
        self.cap = cv2.VideoCapture(self.video_path)
        

        if not self.cap.isOpened():
            raise IOError(f"無法開啟影片: {self.video_path}")


        # Optional: 輸出影片
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.video_output_path, fourcc, 30, (1440, 810))

        # ---------- 資料容器 ----------
        self.pitch_vals = []
        self.yaw_vals = []
        self.roll_vals = []

        self.canvas = MatplotlibWavePlot()  # 初始化繪圖



    # ---------------------------------------------------------
    def run(self, show_window=True, figure_save_path=None):

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # ---- 偵測姿態 ----
            rvec, _, _ = self.detector.detect_face_pose(frame)
            
            if rvec is not None:
                frame = self.detector.annotate_image(frame, rvec)

                angle = self.detector.get_euler_angles(rvec)
                self.pitch_vals.append(angle[0])
                self.yaw_vals.append(angle[1])
                self.roll_vals.append(angle[2])
            
            pitch_recent = self.pitch_vals[-1500:] if self.pitch_vals else []
            yaw_recent = self.yaw_vals[-1500:] if self.yaw_vals else []
            roll_recent = self.roll_vals[-1500:] if self.roll_vals else []
            self.canvas.update_plot(
                pitch_recent,  # 只顯示最近1200個點
                yaw_recent,
                roll_recent,
                np.arange(len(pitch_recent)) / 30  # 假設30 FPS
            )
            buf = self.canvas.canvas.buffer_rgba()
            wave_image = np.asarray(buf)
            wave_image = cv2.cvtColor(wave_image, cv2.COLOR_RGBA2BGR)
            wave_image = cv2.cvtColor(wave_image, cv2.COLOR_RGBA2BGR)
            wave_image = cv2.resize(wave_image, (int(frame.shape[1]*1.5), frame.shape[0]))
            frame = np.hstack((frame, wave_image))
            frame = cv2.resize(frame, (1440, 810))  

            # ---- 寫檔 & 顯示 ----
            if self.writer is not None:
                self.writer.write(frame)

            if show_window:
                cv2.imshow("Pose Tracker", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


        # ---- 收尾 ----
        self.cap.release()
        if self.writer is not None:
            self.writer.release()
            
        if show_window:
            cv2.destroyAllWindows()

        
        self._plot_waveforms(fig_save_path = figure_save_path)


    # ---------------------------------------------------------)

    def _plot_waveforms(self, fig_save_path):
        if not self.pitch_vals:
            print("沒有資料可繪圖。")
            return
        
        self.valid_indices = [i for i, val in enumerate(self.pitch_vals) if not np.isnan(val)]

        self.fps = 30

        times = np.array(self.valid_indices) / self.fps

        # ----- 圖 1：Pitch -----
        fig, axs = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
        axs = axs.flatten()
        for ax in axs:
            ax.set_xlim(0, 10)
            ax.set_ylim(-20, 20)
        

        axs[0].plot(times, self.pitch_vals, label='Pitch', color='red')
        axs[0].set_ylabel("Pitch (deg)")
        axs[0].set_title("Pitch vs. Time")
        axs[0].grid(True)
        axs[1].plot(times, self.yaw_vals, label='Yaw', color='green')
        axs[1].set_ylabel("Yaw (deg)")
        axs[1].set_title("Yaw vs. Time")
        axs[1].grid(True)
        axs[2].plot(times, self.roll_vals, label='Roll', color='blue')
        axs[2].set_xlabel("Time (s)")
        axs[2].set_ylabel("Roll (deg)")
        axs[2].set_title("Roll vs. Time")
        axs[2].grid(True)
        plt.tight_layout()
        plt.savefig(f"{fig_save_path}")
        plt.show()


if __name__ == "__main__":
    video_path = "frames/上.mp4"
    video_output_path = "frames/output上.mp4"
    figure_save_path = "headpose_analysis上.png"
    tracker = PoseTracker(video_path, video_output_path=video_output_path)
    tracker.run(show_window=True, figure_save_path=figure_save_path)
    # 角度調整124行
