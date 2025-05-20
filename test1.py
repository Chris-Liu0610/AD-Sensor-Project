import pyrealsense2 as rs

pipeline = rs.pipeline()
try:
    pipeline.start()
    print(" 相機啟動成功！")
except Exception as e:
    print(f" 相機啟動失敗：{e}")
finally:
    pipeline.stop()
