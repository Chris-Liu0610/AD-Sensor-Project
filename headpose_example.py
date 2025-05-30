import cv2
import numpy as np
import mediapipe as mp
import math
from scipy.spatial.transform import Rotation as R
import pandas as pd

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
        # 基於平均人臉尺寸的3D模型點，往右為負，往左為正，往下為負，往上為正，可變動
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
            rotated_pt = R @ pt
            points_3d.append(rotated_pt)
        
        return np.array(points_3d, dtype=np.float32)
        
    
    def detect_face_pose(self, image):
        """檢測人臉姿態"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb) # 取得人臉網格資訊
        
        if not results.multi_face_landmarks:
            return None, None, None
        
        # 獲取圖像尺寸
        self.setup_camera_matrix()
       
        # 獲取第一張臉的關鍵點
        face_landmarks = results.multi_face_landmarks[0] # 只檢測一張臉
        
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
        object_points = self.get_face_3d_model(tilt_x_degrees = 1, tilt_y_degrees = 2, tilt_z_degrees = 0)
        
        # 使用PnP算法求解姿態
        success, rvec, tvec = cv2.solvePnP(object_points, image_points, self.camera_matrix, self.dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
        # print(rvec)
        
        if not success:
            return None, None, None
        
        
        return rvec, tvec, image_points
    

    def get_euler_angles(self, rvec):
        """將旋轉向量轉換為歐拉角"""
        # 將旋轉向量轉換為旋轉矩陣
        rvec = rvec.flatten()
        r = R.from_rotvec(rvec)
        angle = r.as_euler('xyz', degrees=True)

        # print(angle, end='\r', flush=False)
        print(angle)

        return angle
    
    
    
    def annotate_image(self, image, rvec):
        """在圖像上添加完整的姿態標註"""
        
        annotated = image.copy()
        
        
        # 計算並顯示歐拉角
        angle = self.get_euler_angles(rvec)
        
        # 在圖像上顯示角度信息
        info_text = [
            f"Pitch: {angle[0]:.1f} degree",
            f"Yaw: {angle[1]:.1f} degree",
            f"Roll: {angle[2]:.1f} degree"
        ]
        
        # 背景框
        cv2.rectangle(annotated, (5, 5), (250, 110), (248, 249, 250), -1)
        
        for i, text in enumerate(info_text):
            color = [(51, 51, 255), (51, 255, 51), (255, 51, 51)][i]  # 對應的顏色
            cv2.putText(
                annotated,
                text,
                (15, 35 + i * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2,
                cv2.LINE_AA
            )
        
        
        return annotated


def process_webcam():
    """即時處理網路攝影機影像"""
    detector = FacePoseDetector()
    cap = cv2.VideoCapture(0) # 讀取影片
    
    
    if not cap.isOpened(): 
        print("無法開啟攝影機")
        return
    
    print("按 'q' 退出")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        


        # 檢測人臉姿態
        rvec, tvec, image_points = detector.detect_face_pose(frame)


        
        if rvec is not None:
            # 標註圖像
            frame = detector.annotate_image(frame, rvec)

        # flip the frame for a mirror effect
        # 顯示結果
        cv2.imshow('Face Pose Detection - Triple Arrows', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 使用網路攝影機即時檢測
    process_webcam()
 