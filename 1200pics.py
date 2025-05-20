import cv2
import os

video_path = r"C:/阿茲海默相機/realsense_record/4.mp4"
output_dir = "./frames"
os.makedirs(output_dir, exist_ok=True)


cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise IOError(" 無法開啟影片")

fps = cap.get(cv2.CAP_PROP_FPS)
duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
print(f"影片總長：{duration:.2f} 秒，FPS：{fps}")

target_fps = 30
frame_interval_ms = 1000 / target_fps
frame_count = int(duration * target_fps)

for i in range(frame_count):
    timestamp = i * frame_interval_ms
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp)
    ret, frame = cap.read()
    if not ret:
        print(f" 第 {i} 張失敗")
        continue
    filename = os.path.join(output_dir, f"{i:04d}.png")
    cv2.imwrite(filename, frame)
    print(f" 儲存第 {i} 張 (時間戳: {timestamp:.2f} ms)")

cap.release()
print(" 擷取完成。")
