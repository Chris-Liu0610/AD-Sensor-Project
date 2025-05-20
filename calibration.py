# ✅ RealSense D435 FPS 校正測試程式（儲存每幀影像 + timestamp 差）
import pyrealsense2 as rs
import numpy as np
import cv2
import os

# --- 設定參數 ---
WIDTH = 640
HEIGHT = 480
FPS = 30
FRAME_LIMIT = FPS * 5  # 錄影 5 秒
SAVE_DIR = "calib_frames"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- 初始化 RealSense ---
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, FPS)

print("▶️ 啟動 RealSense...")
profile = pipeline.start(config)

# --- 關閉自動曝光並設定手動曝光 ---
try:
    device = profile.get_device()
    sensors = device.query_sensors()
    for sensor in sensors:
        if sensor.get_info(rs.camera_info.name) == 'RGB Camera':
            sensor.set_option(rs.option.enable_auto_exposure, False)
            sensor.set_option(rs.option.exposure, 100)  # 可調整為 50~200
            sensor.set_option(rs.option.gain, 64)
            print("✅ 曝光與增益設定成功")
except Exception as e:
    print(f"⚠️ 曝光設定失敗：{e}")

print(f"📷 開始錄影 {FRAME_LIMIT} 幀...")

# --- 錄影與 timestamp 測量 ---
frame_count = 0
timestamps = []

while frame_count < FRAME_LIMIT:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    if not color_frame:
        continue

    timestamp = color_frame.get_timestamp()  # 毫秒
    timestamps.append(timestamp)

    frame = np.asanyarray(color_frame.get_data())

    # 儲存影像
    filename = os.path.join(SAVE_DIR, f"frame_{frame_count:03d}_{int(timestamp)}.jpg")
    cv2.imwrite(filename, frame)

    # 顯示畫面與標註
    display = frame.copy()
    cv2.putText(display, f"Frame {frame_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(display, f"Timestamp: {timestamp:.2f} ms", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.imshow("D435 Calibration", display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("⏹️ 提前中止錄影")
        break

    frame_count += 1

# --- 停止設備 ---
pipeline.stop()
cv2.destroyAllWindows()

# --- 根據 timestamp 計算 FPS ---
duration_ms = timestamps[-1] - timestamps[0] if len(timestamps) >= 2 else 0
actual_fps = frame_count / (duration_ms / 1000.0) if duration_ms > 0 else 0

print("\n📊 測試完成：")
print(f"➡️ 總幀數：{frame_count}")
print(f"➡️ timestamp 間距：{duration_ms:.2f} 毫秒")
print(f"➡️ 實際 FPS（依 timestamp）：{actual_fps:.2f} fps")

# --- 輸出每幀 timestamp 差異 ---
print("\n⏱️ 每幀間距（毫秒）:")
for i in range(1, len(timestamps)):
    delta = timestamps[i] - timestamps[i - 1]
    print(f"Frame {i}: Δ {delta:.2f} ms")
