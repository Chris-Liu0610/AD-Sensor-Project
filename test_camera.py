import pyrealsense2 as rs
import numpy as np
import cv2
import time
import os
import re

# 儲存影片資料夾
save_dir = "./realsense_record"
os.makedirs(save_dir, exist_ok=True)

# === 自動取得影片編號檔名 ===
def get_next_video_filename(directory):
    existing = [f for f in os.listdir(directory) if f.endswith('.mp4')]
    numbers = []
    for f in existing:
        match = re.match(r"(\d+)\.mp4", f)
        if match:
            numbers.append(int(match.group(1)))
    next_index = max(numbers) + 1 if numbers else 1
    return os.path.join(directory, f"{next_index}.mp4")

# 取得下一個影片儲存路徑
video_path = get_next_video_filename(save_dir)

# 初始化 RealSense 相機
pipeline = rs.pipeline()
config = rs.config()

# 相機設定（D435）
width, height = 640, 480
fps = 60
duration = 40
frame_count = fps * duration

config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)
pipeline.start(config)

# 初始化影片寫入器（轉 90 度 → 尺寸會互換）
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(video_path, fourcc, fps, (height, width))  # 寬高交換因為旋轉

print(f" 開始錄影並儲存為：{os.path.basename(video_path)}，最長 40 秒，按 Q 可提前結束。")

saved_frames = 0
start_time = time.time()
early_terminated = False

try:
    while saved_frames < frame_count:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.rotate(color_image, cv2.ROTATE_90_CLOCKWISE)

        video_writer.write(color_image)

        cv2.imshow('Recording (Press Q to quit)', color_image)
        saved_frames += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            early_terminated = True
            print(" 錄影已由使用者手動提前終止。")
            break

    if not early_terminated:
        print(f" 錄製完成，總共錄下 {saved_frames} 幀。")
    print(f" 影片已儲存於：{video_path}")

finally:
    pipeline.stop()
    video_writer.release()
    cv2.destroyAllWindows()
    print(" 相機與視窗已關閉。")
