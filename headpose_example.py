import cv2
import numpy as np
import mediapipe as mp
import math
from scipy.spatial.transform import Rotation as R

class FacePoseDetector:
    def __init__(self):
        """初始化人臉姿態檢測器"""
        # 初始化 MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )


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


    def setup_camera_matrix(self, image_width, image_height):
        """設置相機矩陣（如果沒有標定數據，使用估計值）"""
        if self.camera_matrix is None:
            # 估計焦距
            
            # focal_length = (image_width + image_height)/2
            
            # center = (image_width / 2, image_height / 2)
            self.camera_matrix = np.array([
                [385.73846, 0, 324.16235],
                [0, 385.73846, 241.51932],
                [0, 0, 1]
            ], dtype=np.float32)
            
    
    def get_face_3d_model(self):
        """獲取標準人臉3D模型的關鍵點（單位：cm）"""
        # 基於平均人臉尺寸的3D模型點，往右為負，往左為正，往下為負，往上為正
        face_3d_model = {
            'nose_tip': [0.0, 0.0, 0.0],
            'chin': [0.0, -6, -3.0],
            'left_eye_corner': [3.5, 4, -3.0],
            'right_eye_corner': [-3.5, 4, -3.0],
            'left_mouth_corner': [2.5, -1, -2.0],
            'right_mouth_corner': [-2.5, -1, -2.0],
            'forehead': [0.0, 6, -3.0]
        }
        
        # 轉換為numpy數組
        points_3d = [] 
        for key in self.pose_landmarks_indices.keys():
            points_3d.append(face_3d_model[key])
        
        return np.array(points_3d, dtype=np.float32)
        
    
    def detect_face_pose(self, image):
        """檢測人臉姿態"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 取得人臉網格
        results = self.face_mesh.process(image_rgb)
        
        
        if not results.multi_face_landmarks:
            return None, None, None
        
        # 獲取圖像尺寸
        h, w, _ = image.shape
        self.setup_camera_matrix(w, h)
       
        
        # 獲取第一張臉的關鍵點
        face_landmarks = results.multi_face_landmarks[0] # 只檢測一張臉
        # print(face_landmarks)
        
        
        # 提取用於姿態估計的2D點
        image_points = []
        for key, idx in self.pose_landmarks_indices.items():
            landmark = face_landmarks.landmark[idx]
            
            
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            image_points.append([x, y])
        
        
        image_points = np.array(image_points, dtype=np.float32)
        
        # 獲取對應的3D模型點
        object_points = self.get_face_3d_model()
        # print(object_points)
        
        # 使用PnP算法求解姿態
        success, rvec, tvec = cv2.solvePnP(
            object_points,
            image_points,
            self.camera_matrix,
            self.dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )
        


        if not success:
            return None, None, None
        
        # 獲取鼻尖位置（用於繪製箭頭）
        nose_tip_2d = image_points[0]
        # print(image_points)
        
        return rvec, tvec, nose_tip_2d
    
    def draw_rotation_arrows(self, image, rvec, tvec, nose_tip_2d, arrow_length=80):
        """繪製三個分別代表 yaw, roll, pitch 的箭頭"""
        # 獲取歐拉角
        angle = self.get_euler_angles(rvec)
        
        # 定義三個旋轉軸的方向和顏色
        # Yaw: 繞Y軸旋轉（垂直軸），用綠色箭頭表示左右轉動
        # Pitch: 繞X軸旋轉（水平軸），用紅色箭頭表示上下轉動
        # Roll: 繞Z軸旋轉（前後軸），用藍色箭頭表示左右傾斜
        
        # 1. Yaw 箭頭（綠色）- 水平方向
        yaw_angle = math.radians(angle[1])
        yaw_end_x = int(nose_tip_2d[0] + arrow_length * math.sin(yaw_angle))
        yaw_end_y = int(nose_tip_2d[1])
        
        cv2.arrowedLine(
            image,
            (int(nose_tip_2d[0]), int(nose_tip_2d[1])),
            (yaw_end_x, yaw_end_y),
            (0, 255, 0),  # 綠色
            3,
            tipLength=0.3
        )
        cv2.putText(
            image, 
            "Yaw", 
            (yaw_end_x + 10, yaw_end_y),
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.5, 
            (0, 255, 0), 
            2
        )
        
        # 2. Pitch 箭頭（紅色）- 垂直方向
        pitch_angle = math.radians(angle[0])
        pitch_end_x = int(nose_tip_2d[0])
        pitch_end_y = int(nose_tip_2d[1] - arrow_length * math.sin(pitch_angle))
        
        cv2.arrowedLine(
            image,
            (int(nose_tip_2d[0]), int(nose_tip_2d[1])),
            (pitch_end_x, pitch_end_y),
            (0, 0, 255),  # 紅色
            3,
            tipLength=0.3
        )
        cv2.putText(
            image, 
            "Pitch", 
            (pitch_end_x + 10, pitch_end_y),
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.5, 
            (0, 0, 255), 
            2
        )
        
        
        # 繪製鼻尖中心點
        cv2.circle(image, (int(nose_tip_2d[0]), int(nose_tip_2d[1])), 4, (255, 255, 255), -1)
        cv2.circle(image, (int(nose_tip_2d[0]), int(nose_tip_2d[1])), 5, (0, 0, 0), 2)
        
        return image
    
    def draw_combined_arrow(self, image, rvec, tvec, nose_tip_2d, arrow_length=100):
        """繪製一個綜合的方向箭頭（組合了所有旋轉）"""
        # 定義箭頭的3D方向（指向前方）
        arrow_3d = np.array([[0, 0, 0], [0, 0, arrow_length]], dtype=np.float32)
        
        # 將3D箭頭投影到2D圖像平面
        arrow_2d, _ = cv2.projectPoints(
            arrow_3d,
            rvec,
            tvec,
            self.camera_matrix,
            self.dist_coeffs
        )
        
        # 提取箭頭的起點和終點
        arrow_start = tuple(nose_tip_2d.astype(int))
        arrow_end = tuple(arrow_2d[1].ravel().astype(int))
        
        # 繪製綜合方向箭頭（黃色）
        cv2.arrowedLine(
            image,
            arrow_start,
            arrow_end,
            (0, 255, 255),  # 黃色
            5,
            tipLength=0.3
        )
        
        return image
    
    def get_euler_angles(self, rvec):
        """將旋轉向量轉換為歐拉角"""
        # 將旋轉向量轉換為旋轉矩陣
        rmat, _ = cv2.Rodrigues(rvec)
        
        r = R.from_matrix(rmat)
        angle = r.as_euler('xyz', degrees=True)
        # print(rvec)
        print(angle)
        



        return angle
    
    def annotate_image(self, image, rvec, tvec, nose_tip_2d):
        """在圖像上添加完整的姿態標註"""
        annotated = image.copy()
        
        # 繪製三個旋轉箭頭
        annotated = self.draw_rotation_arrows(annotated, rvec, tvec, nose_tip_2d)
        
        # 可選：同時繪製綜合方向箭頭
        # annotated = self.draw_combined_arrow(annotated, rvec, tvec, nose_tip_2d)
        
        # 計算並顯示歐拉角
        angle = self.get_euler_angles(rvec)
        
        # 在圖像上顯示角度信息
        info_text = [
            f"Pitch: {angle[0]:.1f} degree (Red)",
            f"Yaw: {angle[1]:.1f} degree (Green)"
        ]
        
        # 背景框
        cv2.rectangle(annotated, (5, 5), (250, 110), (0, 0, 0), -1)
        cv2.rectangle(annotated, (5, 5), (250, 110), (255, 255, 255), 2)
        
        for i, text in enumerate(info_text):
            color = [(0, 0, 255), (0, 255, 0), (255, 0, 0)][i]  # 對應的顏色
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
        
        # 添加圖例
        legend_y = image.shape[0] - 100
        cv2.putText(
            annotated,
            "Arrow Legend:",
            (10, legend_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )
        cv2.putText(
            annotated,
            "Red: Pitch (Up/Down)",
            (10, legend_y + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
            cv2.LINE_AA
        )
        cv2.putText(
            annotated,
            "Green: Yaw (Left/Right)",
            (10, legend_y + 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
            cv2.LINE_AA
        )

        
        return annotated


def process_webcam():
    """即時處理網路攝影機影像"""
    detector = FacePoseDetector()
    cap = cv2.VideoCapture(0)
    
    
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
        rvec, tvec, nose_tip_2d = detector.detect_face_pose(frame)
        
        if rvec is not None:
            # 標註圖像
            frame = detector.annotate_image(frame, rvec, tvec, nose_tip_2d)

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